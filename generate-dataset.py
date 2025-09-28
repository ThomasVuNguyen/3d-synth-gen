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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tokenizer for counting tokens
try:
    tokenizer = tiktoken.encoding_for_model("gpt-4")
except:
    # Fallback tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")

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

def generate_blender_script(client, object_name: str) -> str:
    """Generate Blender script using AWS Bedrock."""
    try:
        prompt = create_prompt(object_name)
        
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
                response = client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json"
                )
                
                # Parse response
                response_body = json.loads(response['body'].read())
                generated_code = response_body['content'][0]['text']
                
                logger.info(f"Generated script for {object_name} using {model_id}")
                return generated_code
                
            except Exception as model_error:
                logger.warning(f"Model {model_id} failed: {model_error}")
                continue
        
        # If all models fail, return error message
        error_msg = f"# Error: All Bedrock models failed for {object_name}. Please check AWS credentials and model access."
        logger.error(f"All Bedrock models failed for {object_name}")
        return error_msg
        
    except Exception as e:
        logger.error(f"Error generating script for {object_name}: {e}")
        return f"# Error generating script for {object_name}: {str(e)}"

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
    return parser.parse_args()

def main():
    """Main function to generate dataset."""
    try:
        # Parse command line arguments
        args = parse_arguments()

        # Determine count (prioritize positional argument over flag)
        count = args.count if args.count is not None else args.count_flag

        # Load existing results to avoid regenerating
        output_file = 'generated_scripts.json'
        existing_results = load_existing_results(output_file)

        # Setup
        client = setup_bedrock_client()
        objects = read_objects('objects.txt', count)

        # Generate scripts for each object
        results = []
        skipped_count = 0
        generated_count = 0

        for i, object_name in enumerate(objects, 1):
            logger.info(f"Processing object {i}/{len(objects)}: {object_name}")

            # Check if result already exists
            if object_name in existing_results:
                logger.info(f"Skipping {object_name} - already generated")
                result = {
                    "input": object_name,
                    "output": existing_results[object_name]
                }
                skipped_count += 1
            else:
                logger.info(f"Generating new script for {object_name}")
                generated_script = generate_blender_script(client, object_name)
                result = {
                    "input": object_name,
                    "output": generated_script
                }
                generated_count += 1

            results.append(result)

        # Save results
        save_results(results, output_file)

        logger.info("Dataset generation completed successfully!")
        print(f"Processed {len(results)} objects:")
        print(f"- Generated new scripts: {generated_count}")
        print(f"- Skipped existing: {skipped_count}")
        print(f"- Total in output: {len(results)}")

    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == "__main__":
    main()
