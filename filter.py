#!/usr/bin/env python3

import json
import os
import subprocess
import tempfile
import base64
import gc
from datasets import Dataset, Features, Value, Image as HFImage
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

def process_dataset(json_path, num_rows=None, batch_size=100):
    """Process the dataset and create HuggingFace dataset with memory optimization"""

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

    # Process data in batches to manage memory
    datasets = []

    for batch_start in range(0, total_items, batch_size):
        batch_end = min(batch_start + batch_size, total_items)
        batch_data = data[batch_start:batch_end]
        processed_batch = []

        print(f"Processing batch {batch_start//batch_size + 1}/{(total_items + batch_size - 1)//batch_size}")

        for i, item in enumerate(batch_data):
            global_index = batch_start + i
            print(f"Processing item {global_index+1}/{total_items}: {item['input']}")

            # Skip items that already have errors in the output
            if item['output'].startswith("# Error"):
                processed_batch.append({
                    'input': item['input'],
                    'script': None,
                    'image': None,
                    'error': item['output']
                })
                failed += 1
                continue

            # Extract Python script
            script = extract_python_script(item['output'])
            if not script:
                processed_batch.append({
                    'input': item['input'],
                    'script': None,
                    'image': None,
                    'error': "No Python script found in output"
                })
                failed += 1
                continue

            # Create temporary directory for this item
            with tempfile.TemporaryDirectory() as temp_dir:
                image, error = run_blender_pipeline(script, temp_dir)

                processed_batch.append({
                    'input': item['input'],
                    'script': script,
                    'image': image,
                    'error': error
                })

                if image is not None:
                    successful += 1
                else:
                    failed += 1

        # Create dataset from batch and add to list
        batch_dataset = Dataset.from_list(processed_batch, features=features)
        datasets.append(batch_dataset)

        # Clear batch data and force garbage collection
        del processed_batch
        del batch_data
        gc.collect()

        print(f"Batch completed. Memory freed. Progress: {successful} successful, {failed} failed")

    # Concatenate all batch datasets
    print("Combining all batches...")
    if datasets:
        dataset = datasets[0]
        for batch_dataset in datasets[1:]:
            dataset = dataset.concatenate(batch_dataset)
    else:
        dataset = Dataset.from_list([], features=features)

    # Clear batch datasets and force garbage collection
    del datasets
    gc.collect()

    # Save dataset locally
    print("Saving dataset locally...")
    dataset.save_to_disk("3dgen_filtered_dataset")

    # Upload to HuggingFace Hub
    try:
        print("Uploading to HuggingFace Hub...")
        dataset.push_to_hub("ThomasTheMaker/BlenderCAD-Filtered", private=False)
        print("Dataset uploaded to HuggingFace Hub: ThomasTheMaker/BlenderCAD-Filtered")
    except Exception as e:
        print(f"Failed to upload to HuggingFace Hub: {e}")
        print("Dataset saved locally only")

    # Print summary
    print(f"\nProcessing complete:")
    print(f"Total items: {total_items}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    return dataset

if __name__ == "__main__":
    # Process the entire dataset
    dataset = process_dataset("generated_scripts.json")
    print("Dataset saved to '3dgen_filtered_dataset'")

# Read through generated_scripts.json
# Extract the python script, save it as duck.py
# Run blender --background --python duck.py && blender --background --python-expr "import bpy; bpy.ops.import_mesh.stl(filepath='duck.stl'); bpy.context.scene.render.filepath='duck.png'; bpy.ops.render.render(write_still=True)" && chafa duck.png
# Save the data as a huggingface dataset
# If error, save the error to the 'error' column
# If success, save the image to the 'image' column

