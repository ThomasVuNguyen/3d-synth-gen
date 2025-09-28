#!/usr/bin/env python3
"""
Generate 3D Blender scripts using AWS Bedrock Sonnet 4 for objects from objects.txt
"""

import json
import boto3
import logging
import argparse
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from tqdm import tqdm
import tiktoken
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tokenizer for counting tokens
try:
    tokenizer = tiktoken.encoding_for_model("gpt-4")
except:
    # Fallback tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")

# Thread-local storage for clients
thread_local = threading.local()

def setup_bedrock_client():
    """Initialize AWS Bedrock client with credentials."""
    try:
        # Import credentials from credentials.py
        import sys
        sys.path.append('.')
        from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        
        # Configure AWS credentials
        client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        return client
    except Exception as e:
        logger.error(f"Failed to setup Bedrock client: {e}")
        raise

def read_objects(file_path: str, count: int = None) -> List[str]:
    """Read objects from objects.txt file. If count is None, read all objects."""
    try:
        with open(file_path, 'r') as f:
            objects = [line.strip() for line in f if line.strip()]
            if count is not None:
                objects = objects[:count]
        logger.info(f"Read {len(objects)} objects from {file_path}")
        return objects
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        raise
    except Exception as e:
        logger.error(f"Error reading objects: {e}")
        raise

def count_tokens(text: str) -> int:
    """Count tokens in text using tiktoken."""
    try:
        return len(tokenizer.encode(text))
    except Exception as e:
        logger.warning(f"Token counting failed: {e}. Using character approximation.")
        return len(text) // 4  # Rough approximation

def create_prompt(object_name: str) -> str:
    """Create the prompt for generating Blender script."""
    return f"""Create a Blender Python script that constructs a simple 3D model of {object_name} using only primitive meshes (bpy.ops.mesh.primitive_uv_sphere_add, primitive_cube_add, primitive_cone_add, primitive_cylinder_add, etc.), positions and scales them into reasonable proportions, deletes any default objects at the start, groups the parts together, and then exports the model as an ASCII STL file named duck.stl. Return only the runnable Python code, no explanations."""

def get_thread_client():
    """Get or create a Bedrock client for the current thread."""
    if not hasattr(thread_local, 'client'):
        thread_local.client = setup_bedrock_client()
    return thread_local.client

def generate_blender_script_parallel(object_name: str) -> tuple[str, str, int, int, float]:
    """Thread-safe function to generate Blender script. Returns (object_name, script, input_tokens, output_tokens, duration)."""
    start_time = time.time()
    try:
        client = get_thread_client()
        prompt = create_prompt(object_name)
        input_tokens = count_tokens(prompt)

        # Prepare the request body for Claude
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        # Try different models in order of preference (most accessible first)
        models_to_try = [
            "us.anthropic.claude-sonnet-4-20250514-v1:0",     # Claude Sonnet 4 (inference profile)
            "global.anthropic.claude-sonnet-4-20250514-v1:0", # Claude Sonnet 4 (global profile)
            "anthropic.claude-3-haiku-20240307-v1:0",         # Claude 3 Haiku
            "anthropic.claude-3-5-sonnet-20240620-v1:0",      # Claude 3.5 Sonnet
        ]

        for model_id in models_to_try:
            try:
                # Call Bedrock API
                api_start = time.time()
                response = client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json"
                )
                api_duration = time.time() - api_start

                # Parse response
                response_body = json.loads(response['body'].read())
                generated_code = response_body['content'][0]['text']
                output_tokens = count_tokens(generated_code)

                total_duration = time.time() - start_time

                # Print per-query stats
                print(f"📝 {object_name}: {format_time(api_duration)} | 📥 {input_tokens} → 📤 {output_tokens} tokens | {model_id.split('.')[-1]}")

                return object_name, generated_code, input_tokens, output_tokens, total_duration

            except Exception as model_error:
                logger.warning(f"Model {model_id} failed for {object_name}: {model_error}")
                continue

        # If all models fail, return error message
        error_msg = f"# Error: All Bedrock models failed for {object_name}. Please check AWS credentials and model access."
        logger.error(f"All Bedrock models failed for {object_name}")
        total_duration = time.time() - start_time
        print(f"❌ {object_name}: {format_time(total_duration)} | Failed all models")
        return object_name, error_msg, input_tokens, 0, total_duration

    except Exception as e:
        logger.error(f"Error generating script for {object_name}: {e}")
        error_msg = f"# Error generating script for {object_name}: {str(e)}"
        total_duration = time.time() - start_time
        print(f"❌ {object_name}: {format_time(total_duration)} | Error: {str(e)[:50]}...")
        return object_name, error_msg, 0, 0, total_duration

def generate_blender_script(client, object_name: str) -> tuple[str, int, int]:
    """Generate Blender script using AWS Bedrock. Returns (script, input_tokens, output_tokens)."""
    # Legacy function for compatibility - calls the parallel version
    _, script, input_tokens, output_tokens, _ = generate_blender_script_parallel(object_name)
    return script, input_tokens, output_tokens

def load_existing_results(output_file: str) -> Dict[str, str]:
    """Load existing results from JSON file and return as dict {input: output}."""
    try:
        if not os.path.exists(output_file):
            logger.info(f"No existing results file found at {output_file}")
            return {}

        with open(output_file, 'r') as f:
            existing_results = json.load(f)

        # Convert list of results to dict for faster lookup
        existing_dict = {result['input']: result['output'] for result in existing_results}
        logger.info(f"Loaded {len(existing_dict)} existing results from {output_file}")
        return existing_dict
    except Exception as e:
        logger.warning(f"Error loading existing results: {e}. Starting fresh.")
        return {}

def save_results(results: List[Dict[str, Any]], output_file: str):
    """Save results to JSON file."""
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate 3D Blender scripts using AWS Bedrock for objects from objects.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate-dataset.py              # Process all objects
  python generate-dataset.py 100          # Process first 100 objects
  python generate-dataset.py --count 50   # Process first 50 objects
  python generate-dataset.py --workers 8  # Use 8 parallel workers
        """
    )
    parser.add_argument(
        'count',
        nargs='?',
        type=int,
        default=None,
        help='Number of objects to process (default: all objects)'
    )
    parser.add_argument(
        '--count',
        type=int,
        dest='count_flag',
        help='Alternative way to specify number of objects'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4, max: 10)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=20,
        help='Batch size for parallel processing (default: 20)'
    )
    return parser.parse_args()

def format_time(seconds: float) -> str:
    """Format seconds into human-readable time."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def process_batch_parallel(objects_to_generate: List[str], max_workers: int, pbar, results_dict: Dict[str, Dict], lock: threading.Lock, query_times: List[float], all_objects: List[str], existing_results: Dict[str, str], output_file: str) -> tuple[int, int, int]:
    """Process a batch of objects in parallel."""
    total_input_tokens = 0
    total_output_tokens = 0
    generated_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_object = {
            executor.submit(generate_blender_script_parallel, obj): obj
            for obj in objects_to_generate
        }

        # Process completed tasks
        for future in as_completed(future_to_object):
            try:
                object_name, script, input_tokens, output_tokens, duration = future.result()

                with lock:
                    results_dict[object_name] = {
                        "input": object_name,
                        "output": script
                    }
                    generated_count += 1
                    total_input_tokens += input_tokens
                    total_output_tokens += output_tokens
                    query_times.append(duration)

                    # Calculate running averages
                    avg_time = sum(query_times) / len(query_times)

                    pbar.update(1)
                    pbar.set_postfix_str(f"Avg: {format_time(avg_time)} | Workers: {max_workers}")
                    
                    # Save immediately after each object (preserve all existing results)
                    if generated_count % 1 == 0:  # Save every object
                        current_results = []
                        # Include ALL existing results plus any new ones
                        for obj in all_objects:
                            if obj in existing_results:
                                current_results.append({
                                    "input": obj,
                                    "output": existing_results[obj]
                                })
                            elif obj in results_dict:
                                current_results.append(results_dict[obj])
                        save_results(current_results, output_file)

            except Exception as e:
                object_name = future_to_object[future]
                logger.error(f"Error processing {object_name}: {e}")
                with lock:
                    results_dict[object_name] = {
                        "input": object_name,
                        "output": f"# Error generating script for {object_name}: {str(e)}"
                    }
                    pbar.update(1)

    return generated_count, total_input_tokens, total_output_tokens

def main():
    """Main function to generate dataset."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Determine count (prioritize positional argument over flag)
        count = args.count if args.count is not None else args.count_flag

        # Validate and set workers
        max_workers = min(max(1, args.workers), 10)  # Limit to 1-10 workers
        batch_size = max(1, args.batch_size)

        # Load existing results to avoid regenerating
        output_file = 'generated_scripts.json'
        existing_results = load_existing_results(output_file)

        # Setup - read ALL objects first
        all_objects = read_objects('objects.txt', None)
        
        # If count is specified, only process that many from the beginning
        if count is not None:
            objects = all_objects[:count]
        else:
            objects = all_objects

        # Initialize counters
        results = []
        skipped_count = 0
        generated_count = 0
        total_input_tokens = 0
        total_output_tokens = 0

        # Separate existing and new objects
        objects_to_generate = [obj for obj in objects if obj not in existing_results]

        print(f"📊 Processing {len(objects)} objects:")
        print(f"   🔄 New to generate: {len(objects_to_generate)}")
        print(f"   ⏭️  Already exists: {len(objects) - len(objects_to_generate)}")
        print(f"   🧵 Parallel workers: {max_workers}")
        print(f"   📦 Batch size: {batch_size}")
        print()

        # Progress tracking
        start_time = time.time()
        query_times = []  # Track individual query times

        # Create thread-safe results dictionary and lock
        results_dict = {}
        lock = threading.Lock()

        # Add existing results first
        for obj in objects:
            if obj in existing_results:
                results_dict[obj] = {
                    "input": obj,
                    "output": existing_results[obj]
                }
                skipped_count += 1

        # Process new objects in parallel batches
        if objects_to_generate:
            print("🚀 Starting parallel generation...\n")

            with tqdm(total=len(objects), desc="Processing objects",
                     bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                     ncols=100, initial=skipped_count) as pbar:

                # Process in batches
                for i in range(0, len(objects_to_generate), batch_size):
                    batch = objects_to_generate[i:i + batch_size]

                    batch_generated, batch_input_tokens, batch_output_tokens = process_batch_parallel(
                        batch, max_workers, pbar, results_dict, lock, query_times, all_objects, existing_results, output_file
                    )

                    generated_count += batch_generated
                    total_input_tokens += batch_input_tokens
                    total_output_tokens += batch_output_tokens

                    # Note: Individual objects are already saved in process_batch_parallel

        # Convert results dict to ordered list - preserve ALL existing results
        # Start with ALL existing results, then add any new ones
        for obj in all_objects:
            if obj in existing_results:
                # Use existing result
                results.append({
                    "input": obj,
                    "output": existing_results[obj]
                })
            elif obj in results_dict:
                # Use newly generated result
                results.append(results_dict[obj])

        # Save results
        save_results(results, output_file)

        # Final summary
        total_time = time.time() - start_time
        print(f"\n✅ Dataset generation completed!")
        print(f"📈 Summary:")
        print(f"   📝 Total processed: {len(results)} objects")
        print(f"   🆕 Generated new: {generated_count}")
        print(f"   ⏭️  Skipped existing: {skipped_count}")
        print(f"   ⏱️  Total time: {format_time(total_time)}")
        print(f"   🧵 Used {max_workers} parallel workers")

        if generated_count > 0:
            avg_time_per_gen = sum(query_times) / len(query_times) if query_times else 0
            wall_time_per_gen = total_time / generated_count if generated_count > 0 else 0
            print(f"   ⚡ Avg time per query: {format_time(avg_time_per_gen)}")
            print(f"   🕐 Wall time per generation: {format_time(wall_time_per_gen)}")
            speedup = max_workers if total_time > 0 else 1
            print(f"   🚀 Estimated speedup: ~{speedup:.1f}x vs sequential")

        print(f"\n🔢 Token Usage:")
        print(f"   📥 Input tokens: {total_input_tokens:,}")
        print(f"   📤 Output tokens: {total_output_tokens:,}")
        print(f"   📊 Total tokens: {total_input_tokens + total_output_tokens:,}")

        if generated_count > 0:
            print(f"   📊 Avg tokens per object: {(total_input_tokens + total_output_tokens) // generated_count:,}")

    except KeyboardInterrupt:
        print(f"\n⏸️  Generation interrupted by user")
        print(f"📊 Progress saved: {generated_count} objects generated, {skipped_count} skipped")

        # Convert results dict to ordered list for final save
        current_results = []
        for obj in objects:
            if obj in results_dict:
                current_results.append(results_dict[obj])

        if current_results:
            save_results(current_results, output_file)
            print(f"💾 Results saved to {output_file}")
            print(f"📁 Total results in file: {len(current_results)}")
        else:
            print("⚠️  No results to save")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == "__main__":
    main()
