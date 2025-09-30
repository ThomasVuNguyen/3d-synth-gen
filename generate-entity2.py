#!/usr/bin/env python3
"""
Entity Generator Script

Generates entities from scratch using Ollama:
- First generates 2000 unique object names (max 5 duplicates each) saved to txt file
- Then generates descriptions for each object in batches of 4
- Each entity has a concise 1-5 word object name and description under 50 words

Outputs a JSON array where each item has:
  { "object": string, "description": string }

Usage:
  ./generate-entity2.py [count] [names_file] [output_file]

Defaults:
  count = 2000
  names_file = objects_generated.txt
  output_file = entities.json
"""

import json
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests


class EntityGenerator:
    def __init__(self, ollama_url: str = "http://localhost:11434") -> None:
        self.ollama_url = ollama_url
        # Keep model/options consistent with filter-object.py
        self.model = "qwen3:0.6b"
        # No input file; generation is from scratch

    def check_ollama_connection(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                if any(self.model in name for name in model_names):
                    print(f"✓ Found model: {self.model}")
                    return True
                print(f"✗ Model {self.model} not found. Available models: {model_names}")
                return False
            print(f"✗ Ollama connection failed: {response.status_code}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Cannot connect to Ollama: {e}")
            return False

    def call_ollama(self, prompt: str) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "system": (
                    "You are a helpful assistant that completes patterns directly. "
                    "No explanations needed. Respond only in plain text, no markdown formatting."
                ),
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 120,
                    "stop": ["<think>", "\n\n"],
                },
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate", json=payload, timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()

                # Sanitize thinking tags and patterns like "x -> y"
                if "<think>" in response_text and "</think>" in response_text:
                    response_text = response_text.split("</think>")[-1].strip()
                elif "<think>" in response_text:
                    response_text = response_text.split("<think>")[0].strip()

                if "->" in response_text:
                    response_text = response_text.split("->")[-1].strip()

                response_text = response_text.strip('\"\'  \n\r\t')
                response_text = (
                    response_text.replace("*", "").replace("_", "").replace("`", "").replace("#", "")
                )

                if "\n" in response_text:
                    response_text = response_text.split("\n")[0].strip()

                return response_text if response_text else None

            print(f"✗ Ollama API error: {response.status_code} - {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Error calling Ollama: {e}")
            return None

    def create_names_prompt(self, count: int) -> str:
        return (
            "Generate a JSON array with exactly "
            f"{count} strings. Each string is a single word naming a concrete physical object. "
            "Examples: chair, table, lamp, bottle, bowl, box, bag, book, pen, cup, plate, spoon, knife, fork, glass, mug, dish, tray, basket, pot, pan, tool, hammer, screwdriver, wrench, saw, drill, clamp, vise, file, brush, sponge, cloth, towel, blanket, pillow, sheet, curtain, rug, mat, frame, mirror, clock, vase, sculpture, statue, ornament, decoration, toy, game, ball, doll, puzzle, block, card, dice, piece, token, marker, counter. "
            "No brand names, proper nouns, or abstract concepts. No duplicates within the array. "
            "Format: [\"chair\", \"table\", \"lamp\", \"bottle\"]\n"
            "Plain JSON only, no markdown, no code fences, no explanations."
        )

    def create_single_description_prompt(self, object_name: str) -> str:
        return (
            f"Write a detailed description under 50 words describing the parts and components of a {object_name}. "
            "One sentence only, plain text, no lists. "
            "Example: 'A wooden chair with a slatted backrest, four tapered legs, cross-bracing for stability, and a smooth contoured seat with visible grain.'"
        )

    def validate_object_name(self, name: str) -> Optional[str]:
        if not name:
            return None
        words = name.split()
        if len(words) == 0 or len(words) > 5:
            return None
        if len(name) > 80:
            return None
        return name

    def validate_description(self, desc: str) -> Optional[str]:
        if not desc:
            return None
        # Enforce < 50 words strictly
        words = desc.split()
        if len(words) == 0 or len(words) >= 50:
            return None
        # Trim trailing punctuation whitespace
        return desc.strip()

    def parse_and_validate_items(self, data: Any) -> List[Dict[str, str]]:
        valid_items: List[Dict[str, str]] = []
        if not isinstance(data, list):
            return valid_items
        for item in data:
            if not isinstance(item, dict):
                continue
            obj = self.validate_object_name(str(item.get("object", "")).strip())
            desc = self.validate_description(str(item.get("description", "")).strip())
            if obj and desc:
                # Enforce hard limit if needed
                words = desc.split()
                if len(words) >= 50:
                    desc = " ".join(words[:48]) + "."
                valid_items.append({"object": obj, "description": desc})
        return valid_items

    def parse_names(self, text: str) -> List[str]:
        try:
            # Clean up the text first
            text = text.strip()
            
            # Try multiple extraction strategies
            candidates = []
            
            # Strategy 1: Look for JSON array
            start = text.find("[")
            end = text.rfind("]")
            if start != -1 and end != -1 and end > start:
                candidates.append(text[start : end + 1])
            
            # Strategy 2: Look for quoted strings separated by commas
            import re
            quoted_strings = re.findall(r'"([^"]+)"', text)
            if quoted_strings:
                candidates.append(json.dumps(quoted_strings))
            
            # Strategy 3: Look for lines that look like object names
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            object_like_lines = []
            for line in lines:
                # Skip obvious non-object lines
                if any(skip in line.lower() for skip in ['json', 'array', 'generate', 'format', 'example']):
                    continue
                # Look for lines that could be object names (1-5 words, no special chars)
                words = line.split()
                if 1 <= len(words) <= 5 and all(word.replace('-', '').replace("'", '').isalpha() for word in words):
                    object_like_lines.append(line.strip('"\'  \n\r\t'))
            
            if object_like_lines:
                candidates.append(json.dumps(object_like_lines))
            
            # Try each candidate
            for candidate in candidates:
                try:
                    data = json.loads(candidate)
                    if isinstance(data, list) and data:
                        names: List[str] = []
                        for item in data:
                            if isinstance(item, str):
                                cleaned = (item or "").strip().strip('\"\'  \n\r\t')
                                if self.validate_object_name(cleaned):
                                    names.append(cleaned)
                        if names:
                            return names
                except json.JSONDecodeError:
                    continue
            
            return []
        except Exception as e:
            print(f"Parse error: {e}")
            return []

    def request_names_batch(self, count: int, max_retries: int = 3) -> List[str]:
        prompt = self.create_names_prompt(count)
        for attempt in range(1, max_retries + 1):
            text = self.call_ollama(prompt)
            if not text:
                print(f"Attempt {attempt}: empty response for names batch")
                continue
            
            # Debug: show what we got
            print(f"Attempt {attempt}: Raw response: {repr(text[:200])}")
            
            names = self.parse_names(text)
            if names:
                # Deduplicate within the batch while preserving order
                seen: set[str] = set()
                unique_batch: List[str] = []
                for n in names:
                    low = n.lower()
                    if low not in seen:
                        seen.add(low)
                        unique_batch.append(n)
                print(f"Attempt {attempt}: Parsed {len(unique_batch)} unique names")
                return unique_batch[:count]
            print(f"Attempt {attempt}: could not parse names JSON")
        return []

    def generate_fallback_names(self, count: int) -> List[str]:
        """Generate fallback names if model fails completely"""
        base_objects = [
            "chair", "table", "lamp", "bottle", "bowl", "box", "bag", "book", "pen", "cup",
            "plate", "spoon", "knife", "fork", "glass", "mug", "dish", "tray", "basket", "pot",
            "pan", "tool", "hammer", "screwdriver", "wrench", "saw", "drill", "clamp", "vise", "file",
            "brush", "sponge", "cloth", "towel", "blanket", "pillow", "sheet", "curtain", "rug", "mat",
            "frame", "mirror", "clock", "vase", "sculpture", "statue", "ornament", "decoration", "toy", "game",
            "ball", "doll", "puzzle", "block", "card", "dice", "piece", "token", "marker", "counter"
        ]
        
        materials = ["wooden", "metal", "glass", "plastic", "ceramic", "leather", "fabric", "stone", "bamboo", "cardboard"]
        sizes = ["small", "large", "big", "tiny", "huge", "mini", "oversized", "compact", "portable", "heavy"]
        colors = ["red", "blue", "green", "yellow", "black", "white", "brown", "gray", "silver", "golden"]
        
        names = []
        for i in range(count):
            base = base_objects[i % len(base_objects)]
            if i < len(base_objects):
                names.append(base)
            else:
                # Add variety with materials, sizes, colors
                modifier = ""
                if i % 3 == 0 and i < len(materials) * 10:
                    modifier = materials[i % len(materials)] + " "
                elif i % 3 == 1 and i < len(sizes) * 10:
                    modifier = sizes[i % len(sizes)] + " "
                elif i % 3 == 2 and i < len(colors) * 10:
                    modifier = colors[i % len(colors)] + " "
                
                names.append(f"{modifier}{base}")
        
        return names[:count]

    def generate_object_names(self, target_count: int, per_request: int, names_file: Path) -> List[str]:
        print(f"Generating up to {target_count} object names in batches of {per_request}...")
        # Start fresh
        names_file.write_text("", encoding="utf-8")
        names: List[str] = []
        frequency: Dict[str, int] = {}
        attempts = 0
        max_attempts = target_count * 10
        consecutive_failures = 0
        
        while len(names) < target_count and attempts < max_attempts:
            attempts += 1
            batch = self.request_names_batch(per_request)
            if not batch:
                consecutive_failures += 1
                if consecutive_failures >= 10:
                    print("Too many consecutive failures, switching to fallback generation...")
                    fallback_names = self.generate_fallback_names(target_count - len(names))
                    for n in fallback_names:
                        key = n.lower()
                        count = frequency.get(key, 0)
                        if count < 5:
                            names.append(n)
                            frequency[key] = count + 1
                            with names_file.open("a", encoding="utf-8") as f:
                                f.write(n + "\n")
                            if len(names) >= target_count:
                                break
                    break
                continue
            
            consecutive_failures = 0
            added_this_round = 0
            for n in batch:
                key = n.lower()
                count = frequency.get(key, 0)
                if count >= 5:
                    continue
                names.append(n)
                frequency[key] = count + 1
                # Append to file immediately
                with names_file.open("a", encoding="utf-8") as f:
                    f.write(n + "\n")
                added_this_round += 1
                if len(names) >= target_count:
                    break
            if added_this_round == 0:
                # Avoid infinite loop if model keeps repeating
                time.sleep(0.2)
            if len(names) % 100 == 0:
                print(f"  ✓ Collected {len(names)} names so far...")
        print(f"Collected {len(names)} names (attempts: {attempts}).")
        return names[:target_count]

    def generate_descriptions_for_names(self, object_names: List[str]) -> List[Dict[str, str]]:
        print(f"Generating descriptions one by one for {len(object_names)} objects...")
        results: List[Dict[str, str]] = []
        
        for i, name in enumerate(object_names):
            print(f"  [{i+1}/{len(object_names)}] Processing: {name}")
            
            prompt = self.create_single_description_prompt(name)
            text = self.call_ollama(prompt)
            
            if text:
                # Clean up the response
                desc = text.strip().strip('\"\'  \n\r\t')
                # Remove any thinking tags
                if "<think>" in desc and "</think>" in desc:
                    desc = desc.split("</think>")[-1].strip()
                elif "<think>" in desc:
                    desc = desc.split("<think>")[0].strip()
                
                # Validate and enforce word limit
                valid_desc = self.validate_description(desc)
                if valid_desc:
                    results.append({"object": name, "description": valid_desc})
                    print(f"    → {valid_desc}")
                else:
                    # Fallback description
                    fallback = f"A {name} with identifiable components, structural elements, and functional details."
                    results.append({"object": name, "description": fallback})
                    print(f"    → {fallback} (fallback)")
            else:
                # Fallback description
                fallback = f"A {name} with identifiable components, structural elements, and functional details."
                results.append({"object": name, "description": fallback})
                print(f"    → {fallback} (fallback)")
            
            # Progress update every 50 items
            if (i + 1) % 50 == 0:
                print(f"  ✓ Described {len(results)} / {len(object_names)}")
            
            # Small delay to avoid overwhelming the model
            time.sleep(0.1)
        
        return results

    def fallback_items(self, count: int) -> List[Dict[str, str]]:
        seeds = [
            ("wooden chair", "A wooden chair with a slatted backrest, four tapered legs, cross-bracing, and a contoured seat with a clear finish."),
            ("glass bottle", "A clear glass bottle with a narrow threaded neck, cylindrical body, rounded shoulder, and thick base for stability."),
            ("metal toolbox", "A steel toolbox featuring a hinged lid, removable tray, latch closures, corner reinforcements, and a fold-down handle."),
            ("ceramic bowl", "A glazed ceramic bowl with a wide rim, smooth interior, curved walls, and a small foot ring for balance."),
            ("desk lamp", "An adjustable desk lamp with a weighted base, articulated arm, swivel head, heat venting, and an inline switch."),
        ]
        out: List[Dict[str, str]] = []
        i = 0
        while len(out) < count:
            name, desc = seeds[i % len(seeds)]
            out.append({"object": name, "description": desc})
            i += 1
        return out[:count]

    def generate(self, count: int, names_file: Path, per_request: int = 4) -> List[Dict[str, Any]]:
        names = self.generate_object_names(target_count=count, per_request=per_request, names_file=names_file)
        entities = self.generate_descriptions_for_names(names)
        print(f"\n✓ Generation complete! Created {len(entities)} entities.")
        return entities


def main() -> None:
    print("Entity Generator Script")
    print("=" * 30)

    count = 2000
    names_file = "objects_generated.txt"
    output_file = "entities.json"

    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Invalid count. Using default: 2000")

    if len(sys.argv) > 2:
        names_file = sys.argv[2]
    if len(sys.argv) > 3:
        output_file = sys.argv[3]

    generator = EntityGenerator()
    if not generator.check_ollama_connection():
        print("Please ensure Ollama is running and the model is available.")
        return

    entities = generator.generate(count=count, names_file=Path(names_file), per_request=4)

    out_path = Path(output_file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved to {out_path}")


if __name__ == "__main__":
    main()


