#!/usr/bin/env python3

import json
import os
import subprocess
import tempfile
import base64
import gc
from multiprocessing import Pool, cpu_count
from functools import partial
from datasets import Dataset, Features, Value, Image as HFImage, concatenate_datasets
from PIL import Image
import io

def extract_python_script(output_text):
    """Extract Python script from markdown code blocks"""
    if "```python" in output_text:
        start = output_text.find("```python") + 9
        end = output_text.find("```", start)
        return output_text[start:end].strip()
    return None

def run_blender_pipeline(script_content, temp_dir):
    """Run the Blender pipeline and return result"""
    try:
        # Save script as duck.py
        script_path = os.path.join(temp_dir, "duck.py")
        with open(script_path, 'w') as f:
            f.write(script_content)

        # Run blender to generate STL
        cmd1 = ["blender", "--background", "--python", script_path]
        result1 = subprocess.run(cmd1, capture_output=True, text=True, cwd=temp_dir, timeout=60)

        if result1.returncode != 0:
            return None, f"Blender script failed: {result1.stderr}"

        # Check if STL was created
        stl_path = os.path.join(temp_dir, "duck.stl")
        if not os.path.exists(stl_path):
            return None, "STL file was not generated"

        # Run blender to render PNG
        render_cmd = f"import bpy; bpy.ops.import_mesh.stl(filepath='duck.stl'); bpy.context.scene.render.filepath='duck.png'; bpy.ops.render.render(write_still=True)"
        cmd2 = ["blender", "--background", "--python-expr", render_cmd]
        result2 = subprocess.run(cmd2, capture_output=True, text=True, cwd=temp_dir, timeout=60)

        if result2.returncode != 0:
            return None, f"Blender render failed: {result2.stderr}"

        # Check if PNG was created
        png_path = os.path.join(temp_dir, "duck.png")
        if not os.path.exists(png_path):
            return None, "PNG file was not generated"

        # Load image and save to bytes in memory
        with open(png_path, 'rb') as f:
            img_bytes = f.read()

        # Create PIL Image from bytes
        image = Image.open(io.BytesIO(img_bytes))
        # Convert to RGB if needed (removes alpha channel)
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Clean up temporary files to free disk space
        try:
            os.remove(stl_path)
            os.remove(png_path)
        except:
            pass

        return image, None

    except subprocess.TimeoutExpired:
        return None, "Blender process timed out"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
    finally:
        # Force garbage collection after each Blender run
        gc.collect()

def process_single_item(item_data):
    """Worker function to process a single item - designed for multiprocessing"""
    item, index = item_data

    try:
        print(f"Processing item {index}: {item['input']}")

        # Skip items that already have errors in the output
        if item['output'].startswith("# Error"):
            return {
                'input': item['input'],
                'script': None,
                'image': None,
                'error': item['output']
            }

        # Extract Python script
        script = extract_python_script(item['output'])
        if not script:
            return {
                'input': item['input'],
                'script': None,
                'image': None,
                'error': "No Python script found in output"
            }

        # Create temporary directory for this item
        with tempfile.TemporaryDirectory() as temp_dir:
            image, error = run_blender_pipeline(script, temp_dir)

            return {
                'input': item['input'],
                'script': script,
                'image': image,
                'error': error
            }
    except Exception as e:
        return {
            'input': item['input'],
            'script': None,
            'image': None,
            'error': f"Processing error: {str(e)}"
        }

def process_dataset(json_path, num_rows=None, batch_size=100, save_every=100, num_workers=None):
    """Process the dataset and save parquet files every N rows with parallel processing and memory optimization"""

    # Set default number of workers (leave 1 CPU free for system)
    if num_workers is None:
        num_workers = max(1, cpu_count() - 1)

    print(f"Using {num_workers} parallel workers")
    print(f"Saving parquet files every {save_every} rows")

    # Read the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Limit to first num_rows if specified
    if num_rows is not None:
        data = data[:num_rows]

    # Define dataset features with proper Image type
    features = Features({
        'input': Value('string'),
        'script': Value('string'),
        'image': HFImage(),
        'error': Value('string')
    })

    # Initialize counters
    total_items = len(data)
    successful = 0
    failed = 0
    parquet_file_count = 0
    accumulated_data = []

    # Create output directory
    output_dir = "3dgen_filtered_parquets"
    os.makedirs(output_dir, exist_ok=True)

    for batch_start in range(0, total_items, batch_size):
        batch_end = min(batch_start + batch_size, total_items)
        batch_data = data[batch_start:batch_end]

        print(f"Processing batch {batch_start//batch_size + 1}/{(total_items + batch_size - 1)//batch_size} ({len(batch_data)} items)")

        # Prepare data for parallel processing (item, global_index)
        batch_items_with_index = [(item, batch_start + i) for i, item in enumerate(batch_data)]

        # Process batch in parallel
        with Pool(processes=num_workers) as pool:
            processed_batch = pool.map(process_single_item, batch_items_with_index)

        # Count successful and failed items
        for item in processed_batch:
            if item['image'] is not None:
                successful += 1
            else:
                failed += 1

        # Add processed batch to accumulated data
        accumulated_data.extend(processed_batch)

        # Save parquet file if we have enough data
        if len(accumulated_data) >= save_every:
            # Take exactly save_every items for this parquet file
            parquet_data = accumulated_data[:save_every]
            remaining_data = accumulated_data[save_every:]

            # Create dataset and save as parquet
            parquet_dataset = Dataset.from_list(parquet_data, features=features)
            parquet_filename = f"filtered_dataset_{parquet_file_count:04d}.parquet"
            parquet_path = os.path.join(output_dir, parquet_filename)
            parquet_dataset.to_parquet(parquet_path)

            print(f"Saved {parquet_filename} with {len(parquet_data)} rows")

            # Note: HuggingFace upload will happen at the end

            # Clean up
            del parquet_dataset
            del parquet_data
            parquet_file_count += 1
            accumulated_data = remaining_data

        # Clear batch data and force garbage collection
        del processed_batch
        del batch_data
        del batch_items_with_index
        gc.collect()

        print(f"Batch completed. Memory freed. Progress: {successful} successful, {failed} failed")

    # Save any remaining data
    if accumulated_data:
        parquet_dataset = Dataset.from_list(accumulated_data, features=features)
        parquet_filename = f"filtered_dataset_{parquet_file_count:04d}.parquet"
        parquet_path = os.path.join(output_dir, parquet_filename)
        parquet_dataset.to_parquet(parquet_path)

        print(f"Saved final {parquet_filename} with {len(accumulated_data)} rows")

        # Note: HuggingFace upload will happen at the end

        del parquet_dataset
        parquet_file_count += 1

    # Print summary
    print(f"\nProcessing complete:")
    print(f"Total items: {total_items}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Parquet files created: {parquet_file_count}")
    print(f"Files saved in: {output_dir}")

    # Upload all parquet files as a single dataset to HuggingFace Hub
    print("Uploading complete dataset to HuggingFace Hub...")
    try:
        from datasets import load_dataset
        # Load all parquet files as a single dataset
        full_dataset = load_dataset("parquet", data_dir=output_dir, split="train")
        full_dataset.push_to_hub(
            "ThomasTheMaker/BlenderCAD-Filtered",
            private=False
        )
        print("Successfully uploaded complete dataset to HuggingFace Hub")
    except Exception as e:
        print(f"Failed to upload dataset to HuggingFace Hub: {e}")

    return parquet_file_count

if __name__ == "__main__":
    # Process the entire dataset with parallel processing
    # You can customize these parameters:
    # - num_rows: limit processing to first N rows (None for all)
    # - batch_size: items per batch (100 is good for memory management)
    # - num_workers: parallel processes (None for auto-detection)

    parquet_count = process_dataset(
        json_path="generated_scripts.json",
        num_rows=None,  # Process all rows
        batch_size=50,  # Smaller batches for better parallelization
        save_every=100,  # Save parquet file every 100 rows
        num_workers=None  # Auto-detect CPU count
    )
    print(f"Processing complete! Created {parquet_count} parquet files in '3dgen_filtered_parquets' directory")

# Read through generated_scripts.json
# Extract the python script, save it as duck.py
# Run blender --background --python duck.py && blender --background --python-expr "import bpy; bpy.ops.import_mesh.stl(filepath='duck.stl'); bpy.context.scene.render.filepath='duck.png'; bpy.ops.render.render(write_still=True)" && chafa duck.png
# Save the data as a huggingface dataset
# If error, save the error to the 'error' column
# If success, save the image to the 'image' column

