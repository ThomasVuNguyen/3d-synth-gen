#!/usr/bin/env python3
"""
Object Filter and Rephrasing Script

This script reads objects from objects.txt line by line, uses Qwen3:4b on Ollama
to rephrase each object into a common object name (under 5 words), and generates
adjacent objects with good names.
"""

import requests
import json
import time
import sys
from pathlib import Path
from typing import List, Tuple, Optional

class ObjectFilter:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "gemma3:1b"  # Using qwen2.5:4b as qwen3:4b might not be available
        self.input_file = "objects.txt"
        self.output_file = "filtered_objects.txt"
        
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                if any(self.model in name for name in model_names):
                    print(f"✓ Found model: {self.model}")
                    return True
                else:
                    print(f"✗ Model {self.model} not found. Available models: {model_names}")
                    return False
            else:
                print(f"✗ Ollama connection failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Cannot connect to Ollama: {e}")
            return False
    
    def call_ollama(self, prompt: str) -> Optional[str]:
        """Call Ollama API to get response from the model."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "system": "You are a helpful assistant that completes patterns directly. No explanations needed. Respond only in plain text, no markdown formatting.",
                "options": {
                    "temperature": 0.1,  # Lower temperature for consistency
                    "top_p": 0.9,
                    "num_predict": 80,   # Allow more tokens for longer descriptions
                    "stop": ["<think>", "\n\n"]  # Only stop on thinking or double newline
                }
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30  # Add reasonable timeout
            )

            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()

                print(f"    Raw response: '{response_text}'")

                # Handle thinking tags more carefully
                if "<think>" in response_text and "</think>" in response_text:
                    # Extract text after </think>
                    response_text = response_text.split("</think>")[-1].strip()
                elif "<think>" in response_text:
                    # If unclosed think tag, remove everything up to it
                    response_text = response_text.split("<think>")[0].strip()

                # Extract answer after arrow if present
                if "->" in response_text:
                    response_text = response_text.split("->")[-1].strip()

                # Clean up quotes, extra whitespace, and any markdown formatting
                response_text = response_text.strip('"\'  \n\r\t')
                # Remove any markdown formatting
                response_text = response_text.replace('*', '').replace('_', '').replace('`', '').replace('#', '')

                # Take first line if multiple lines
                if '\n' in response_text:
                    response_text = response_text.split('\n')[0].strip()

                # Validate response
                if not response_text:
                    print(f"    Warning: Empty response")
                    return None
                elif len(response_text) > 80:
                    print(f"    Warning: Response too long: '{response_text[:50]}...'")
                    return None
                elif len(response_text.split()) > 5:
                    print(f"    Warning: Too many words: '{response_text}'")
                    return None

                return response_text
            else:
                print(f"✗ Ollama API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"✗ Error calling Ollama: {e}")
            return None
    
    def create_rephrase_prompt(self, object_name: str) -> str:
        """Create a prompt to rephrase the object into a common name under 5 words."""
        return f"""Complete the pattern with a proper object description (adjective + noun). 2-5 words only. No thinking, just the answer. No markdown formatting, only plain text:

abs bag -> leather handbag
abs chair -> wooden chair
abs lamp -> desk lamp
abs bowl -> ceramic bowl
abs bottle -> glass bottle
abs table -> oak table
abs mirror -> wall mirror
abs clock -> grandfather clock
abs basket -> wicker basket
abs bed -> queen bed

{object_name} ->"""
    
    def create_adjacent_prompt(self, rephrased_object: str) -> str:
        """Create a prompt to generate an adjacent object."""
        return f"""Complete the pattern with a proper object description (adjective + noun). 2-5 words only. No thinking, just the answer. No markdown formatting, only plain text:

leather handbag -> leather wallet
wooden chair -> wooden table
desk lamp -> desk organizer
ceramic bowl -> wooden spoon
glass bottle -> wine glass
oak table -> wooden chairs
wall mirror -> wall sconces
grandfather clock -> wall clock
wicker basket -> picnic blanket
queen bed -> down pillow

{rephrased_object} ->"""
    
    def process_objects(self, start_line: int = 1, max_lines: int = 100) -> None:
        """Process objects from the input file."""
        if not self.check_ollama_connection():
            print("Please ensure Ollama is running and the model is available.")
            return
        
        input_path = Path(self.input_file)
        if not input_path.exists():
            print(f"✗ Input file {self.input_file} not found.")
            return
        
        print(f"Processing objects from line {start_line} to {start_line + max_lines - 1}")
        print("=" * 60)
        
        with open(input_path, 'r', encoding='utf-8') as infile, \
             open(self.output_file, 'w', encoding='utf-8') as outfile:
            
            # Skip to start line
            for _ in range(start_line - 1):
                infile.readline()
            
            processed = 0
            for line_num, line in enumerate(infile, start=start_line):
                if processed >= max_lines:
                    break
                
                original_object = line.strip()
                if not original_object:
                    continue
                
                print(f"\n[{line_num}] Processing: {original_object}")
                
                # Step 1: Rephrase the object
                rephrase_prompt = self.create_rephrase_prompt(original_object)
                rephrased = self.call_ollama(rephrase_prompt)
                
                if not rephrased:
                    print(f"  ✗ Failed to rephrase: {original_object}")
                    # Fallback: use intelligent conversion with proper object descriptions
                    base_word = original_object.split()[-1] if ' ' in original_object else original_object
                    if base_word == "bag":
                        rephrased = "leather handbag"
                    elif base_word == "chair":
                        rephrased = "wooden chair"
                    elif base_word == "lamp":
                        rephrased = "desk lamp"
                    elif base_word == "bowl":
                        rephrased = "ceramic bowl"
                    elif base_word == "basket":
                        rephrased = "wicker basket"
                    elif base_word == "bed":
                        rephrased = "queen bed"
                    elif base_word == "bottle":
                        rephrased = "glass bottle"
                    elif base_word == "box":
                        rephrased = "wooden box"
                    elif base_word == "table":
                        rephrased = "oak table"
                    elif base_word == "mirror":
                        rephrased = "wall mirror"
                    elif base_word == "clock":
                        rephrased = "grandfather clock"
                    else:
                        rephrased = f"wooden {base_word}"
                    print(f"  → Fallback rephrased: {rephrased}")
                
                print(f"  → Rephrased: {rephrased}")
                
                # Step 2: Generate adjacent object
                adjacent_prompt = self.create_adjacent_prompt(rephrased)
                adjacent = self.call_ollama(adjacent_prompt)
                
                if not adjacent:
                    print(f"  ✗ Failed to generate adjacent object")
                    # Fallback: use intelligent related objects with proper object descriptions
                    if 'bag' in rephrased.lower() or 'handbag' in rephrased.lower():
                        adjacent = "leather wallet"
                    elif 'chair' in rephrased.lower():
                        adjacent = "wooden table"
                    elif 'lamp' in rephrased.lower():
                        adjacent = "desk organizer"
                    elif 'bowl' in rephrased.lower():
                        adjacent = "wooden spoon"
                    elif 'basket' in rephrased.lower():
                        adjacent = "picnic blanket"
                    elif 'bed' in rephrased.lower():
                        adjacent = "down pillow"
                    elif 'bottle' in rephrased.lower():
                        adjacent = "wine glass"
                    elif 'box' in rephrased.lower():
                        adjacent = "storage lid"
                    elif 'table' in rephrased.lower():
                        adjacent = "wooden chairs"
                    elif 'mirror' in rephrased.lower():
                        adjacent = "wall sconces"
                    elif 'clock' in rephrased.lower():
                        adjacent = "wall clock"
                    else:
                        adjacent = "wooden item"
                    print(f"  → Fallback adjacent: {adjacent}")
                
                print(f"  → Adjacent: {adjacent}")
                
                # Write results - one object per line
                outfile.write(f"{rephrased}\n")
                outfile.write(f"{adjacent}\n")
                outfile.flush()
                
                processed += 1
                
                # Add small delay to avoid overwhelming the API
                time.sleep(0.5)
                
                if processed % 10 == 0:
                    print(f"  ✓ Processed {processed} objects so far...")
        
        print(f"\n✓ Processing complete! Results saved to {self.output_file}")
        print(f"✓ Processed {processed} objects")

def main():
    """Main function to run the object filter."""
    print("Object Filter and Rephrasing Script")
    print("=" * 40)
    
    # Parse command line arguments
    start_line = 1
    max_lines = 100
    
    if len(sys.argv) > 1:
        try:
            start_line = int(sys.argv[1])
        except ValueError:
            print("Invalid start line number. Using default: 1")
    
    if len(sys.argv) > 2:
        try:
            max_lines = int(sys.argv[2])
        except ValueError:
            print("Invalid max lines number. Using default: 100")
    
    # Create and run the filter
    filter_obj = ObjectFilter()
    filter_obj.process_objects(start_line=start_line, max_lines=max_lines)

if __name__ == "__main__":
    main()
