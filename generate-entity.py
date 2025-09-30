#!/usr/bin/env python3
"""
Entity Generator Script

Generates entities from scratch using Ollama:
- First generates 2000 unique object names (max 5 duplicates each) saved to txt file
- Then generates descriptions for each object in batches of 4
- Each entity has a creative 3-7 word object name and description under 50 words

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
        # Use a more capable model for generation
        self.model = "llama3.2:3b"
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
                    "You are a helpful assistant that generates JSON arrays of object names. "
                    "Output only valid JSON, no explanations, no markdown."
                ),
                "options": {
                    "temperature": 1.0,
                    "top_p": 0.95,
                    "num_predict": 200,
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
            f"{count} strings. Each string is 3-7 words describing a simple concrete 3D object that someone would ask AI to generate. Keep objects simple and straightforward. Vary the length. "
            "Examples: wooden chair, coffee mug, table lamp, flower vase, storage box, backpack, helmet, dinner plate, wall clock, picture frame, ceramic bowl, desk organizer. "
            "Be creative but keep objects simple and common. Vary the word count (3-7 words). No brand names or proper nouns. No duplicates within the array. "
            "Format: [\"wooden chair\", \"coffee mug\", \"table lamp\"]\n"
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
        if len(words) < 3 or len(words) > 7:
            return None
        if len(name) > 100:
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
                # Look for lines that are 3-7 words
                words = line.split()
                if 3 <= len(words) <= 7 and all(word.replace('-', '').replace("'", '').isalpha() for word in words):
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

    def generate_fallback_names_DISABLED(self, count: int) -> List[str]:
        """Generate fallback names if model fails completely"""
        base_objects = [
            "chair", "table", "lamp", "mug", "vase", "box", "backpack",
            "notebook", "pencil", "cup", "plate", "knife", "spoon",
            "frame", "clock", "bowl", "basket", "pot", "pan",
            "shelf", "cabinet", "mirror", "pillow", "blanket", "rug",
            "bottle", "jar", "candle", "lantern", "trophy", "medal",
            "ball", "dice", "toy", "book", "pen", "eraser",
            "scissors", "stapler", "ruler", "folder", "tray", "coaster",
            "hook", "hanger", "container", "holder", "stand", "rack"
        ]

        materials = ["wooden", "metal", "glass", "plastic", "ceramic", "fabric", "leather", "paper", "bamboo", "stone"]
        styles = ["simple", "modern", "vintage", "small", "large", "round", "square", "tall", "short", "wide"]
        extras = ["with handle", "with lid", "with base", "with stand", "with drawer", "with pattern", "for desk", "for wall", "for kitchen", "for office"]

        names = []
        for i in range(count):
            base = base_objects[i % len(base_objects)]

            # Vary length: 3, 4, 5, 6, or 7 words
            length_pattern = i % 5

            if length_pattern == 0:  # 2 words (simple)
                material = materials[i % len(materials)]
                names.append(f"{material} {base}")
            elif length_pattern == 1:  # 3 words
                style = styles[i % len(styles)]
                names.append(f"{style} {material} {base}")
            elif length_pattern == 2:  # 4 words
                material = materials[i % len(materials)]
                extra_word = extras[i % len(extras)].split()[0]
                names.append(f"{material} {base} {extra_word} handle")
            elif length_pattern == 3:  # 5 words
                material = materials[i % len(materials)]
                extra = extras[i % len(extras)]
                names.append(f"{material} {base} {extra}")
            else:  # 6-7 words
                style = styles[i % len(styles)]
                material = materials[(i // len(styles)) % len(materials)]
                extra = extras[i % len(extras)]
                names.append(f"{style} {material} {base} {extra}")

        return names[:count]

    def generate_object_names(self, target_count: int, per_request: int, names_file: Path) -> List[str]:
        # Check if we can resume from existing file
        existing_names: List[str] = []
        frequency: Dict[str, int] = {}

        if names_file.exists():
            existing_names = names_file.read_text(encoding="utf-8").strip().split("\n")
            existing_names = [n.strip() for n in existing_names if n.strip()]
            for name in existing_names:
                key = name.lower()
                frequency[key] = frequency.get(key, 0) + 1
            if len(existing_names) >= target_count:
                print(f"Found {len(existing_names)} existing names in {names_file}, using those.")
                return existing_names[:target_count]
            print(f"Resuming from {len(existing_names)} existing names...")
        else:
            print(f"Generating up to {target_count} object names in batches of {per_request}...")
            names_file.write_text("", encoding="utf-8")

        names: List[str] = existing_names
        attempts = 0
        max_attempts = target_count * 10
        consecutive_failures = 0
        start_time = time.time()

        while len(names) < target_count and attempts < max_attempts:
            attempts += 1
            batch = self.request_names_batch(per_request)
            if not batch:
                consecutive_failures += 1
                if consecutive_failures >= 10:
                    print("Too many consecutive failures. Stopping generation.")
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
            if len(names) % 100 == 0 and len(names) > 0:
                elapsed = time.time() - start_time
                rate = len(names) / elapsed
                remaining = target_count - len(names)
                eta_seconds = remaining / rate if rate > 0 else 0
                eta_minutes = eta_seconds / 60
                print(f"  ✓ Collected {len(names)}/{target_count} names | ETA: {eta_minutes:.1f} min")

        elapsed = time.time() - start_time
        print(f"Collected {len(names)} names in {elapsed:.1f}s (attempts: {attempts}).")
        return names[:target_count]

    def generate_descriptions_for_names(self, object_names: List[str]) -> List[Dict[str, str]]:
        if not object_names:
            return []

        print(f"Generating descriptions one by one for {len(object_names)} objects...")
        results: List[Dict[str, str]] = []
        start_time = time.time()

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
                    print(f"    → (skipped - invalid description)")
            else:
                print(f"    → (skipped - no response)")
            
            # Progress update every 50 items
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                remaining = len(object_names) - (i + 1)
                eta_seconds = remaining / rate if rate > 0 else 0
                eta_minutes = eta_seconds / 60
                print(f"  ✓ Described {len(results)}/{len(object_names)} | ETA: {eta_minutes:.1f} min")

            # Small delay to avoid overwhelming the model
            time.sleep(0.1)

        elapsed = time.time() - start_time
        print(f"Generated {len(results)} descriptions in {elapsed:.1f}s")
        return results

    def fallback_items_DISABLED(self, count: int) -> List[Dict[str, str]]:
        seeds = [
            ("wooden chair", "A wooden chair with four legs, a backrest, smooth seat surface, rounded edges, and simple construction."),
            ("coffee mug", "A coffee mug with a cylindrical body, curved handle, thick walls for heat retention, rounded rim, and flat base."),
            ("table lamp", "A table lamp with a round base, vertical pole, lamp shade, light socket, and power cord with switch."),
            ("flower vase", "A flower vase with a narrow neck, wide opening, rounded body, smooth glazed surface, and stable bottom."),
            ("storage box", "A storage box with four sides, a hinged lid, latch closure, sturdy corners, and handles for carrying."),
            ("ceramic bowl", "A ceramic bowl with smooth interior, rounded walls, wide rim, glazed finish, and circular base for stability."),
            ("picture frame", "A picture frame with four rectangular sides, glass front, backing board, mounting hardware, and hanging hook on back."),
        ]
        out: List[Dict[str, str]] = []
        i = 0
        while len(out) < count:
            name, desc = seeds[i % len(seeds)]
            out.append({"object": name, "description": desc})
            i += 1
        return out[:count]

    def generate(self, count: int, names_file: Path, output_file: Path, per_request: int = 10) -> List[Dict[str, Any]]:
        # Check if output file exists and can be resumed
        existing_entities: List[Dict[str, Any]] = []
        if output_file.exists():
            try:
                with open(output_file, "r", encoding="utf-8") as f:
                    existing_entities = json.load(f)
                if len(existing_entities) >= count:
                    print(f"Found {len(existing_entities)} existing entities in {output_file}, skipping generation.")
                    return existing_entities[:count]
                print(f"Found {len(existing_entities)} existing entities, will continue from there...")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Could not load existing entities: {e}")
                existing_entities = []

        names = self.generate_object_names(target_count=count, per_request=per_request, names_file=names_file)

        # Extract already processed names from existing entities
        processed_names = {e["object"] for e in existing_entities}
        remaining_names = [n for n in names if n not in processed_names]

        if remaining_names:
            print(f"Generating descriptions for {len(remaining_names)} remaining objects...")
            new_entities = self.generate_descriptions_for_names(remaining_names)
            entities = existing_entities + new_entities
        else:
            print("All names already have descriptions.")
            entities = existing_entities

        print(f"\n✓ Generation complete! Created {len(entities)} entities.")
        return entities


def main() -> None:
    print("Entity Generator Script")
    print("=" * 30)

    count = 5000
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

    entities = generator.generate(count=count, names_file=Path(names_file), output_file=Path(output_file), per_request=10)

    out_path = Path(output_file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved to {out_path}")


if __name__ == "__main__":
    main()


