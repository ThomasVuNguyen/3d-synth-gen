#!/usr/bin/env python3
"""
Generate 3D models from entities.json:
1. Take an object and description from entities.json
2. Generate blender python code similar to v1/generate-dataset.py
3. Run the blender python code with render.py to get a render.png
4. If failed, try again with the same object for 10 times until success or reach the limit
5. Save the generated image on the column 'image' of a database
6. Save the code on the column 'code' of a database
7. After 10 objects, upload to ThomasTheMaker/BlenderCAD2 --repo-type=dataset
"""

import json
import os
import subprocess
import tempfile
import time
import sqlite3
import logging
from typing import Dict, Optional, Tuple
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MAX_RETRIES = 10
BATCH_SIZE = 10
DB_FILE = 'generated_models.db'
HF_REPO = 'ThomasTheMaker/BlenderCAD2'

def setup_database():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            object TEXT PRIMARY KEY,
            description TEXT,
            code TEXT,
            image BLOB
        )
    ''')
    conn.commit()
    return conn

def setup_bedrock_client():
    """Initialize AWS Bedrock client with credentials."""
    try:
        from credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

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

def load_entities(file_path: str = 'entities.json', offset: int = 0, limit: Optional[int] = None) -> list:
    """Load entities from JSON file."""
    try:
        with open(file_path, 'r') as f:
            entities = json.load(f)

        if limit:
            return entities[offset:offset + limit]
        return entities[offset:]
    except Exception as e:
        logger.error(f"Error loading entities: {e}")
        raise

def create_prompt(object_name: str, description: str) -> str:
    """Create the prompt for generating Blender script."""
    return f"""Create a Blender Python script that constructs a detailed 3D model of {object_name}.

Description: {description}

Requirements:
- Use primitive meshes (bpy.ops.mesh.primitive_uv_sphere_add, primitive_cube_add, primitive_cone_add, primitive_cylinder_add, etc.)
- Position and scale them into reasonable proportions based on the description
- Delete any default objects at the start
- Group the parts together
- Export the model as an ASCII STL file named duck.stl

Return only the runnable Python code, no explanations."""

def generate_blender_code(client, object_name: str, description: str) -> Optional[str]:
    """Generate Blender script using AWS Bedrock."""
    try:
        prompt = create_prompt(object_name, description)

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

        models_to_try = [
            "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "global.anthropic.claude-sonnet-4-20250514-v1:0",
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0",
        ]

        for model_id in models_to_try:
            try:
                response = client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json"
                )

                response_body = json.loads(response['body'].read())
                generated_code = response_body['content'][0]['text']

                logger.info(f"✅ Generated code for '{object_name}' using {model_id}")
                return generated_code

            except Exception as model_error:
                logger.warning(f"Model {model_id} failed: {model_error}")
                continue

        logger.error(f"All models failed for '{object_name}'")
        return None

    except Exception as e:
        logger.error(f"Error generating code for '{object_name}': {e}")
        return None

def extract_script_code(output_text: str) -> str:
    """Extract Python code from the output text (removes markdown formatting)."""
    lines = output_text.split('\n')
    code_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith('```python') or line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        elif in_code_block or (not any(line.strip().startswith(x) for x in ['```', '#'])):
            code_lines.append(line)

    return '\n'.join(code_lines)

def run_blender_script(script_code: str, object_name: str) -> bool:
    """Run the Blender script to generate STL."""
    logger.info(f"🎨 Running Blender script for: {object_name}")

    # Extract clean code
    clean_code = extract_script_code(script_code)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(clean_code)
        script_path = f.name

    try:
        cmd = ['blender', '--background', '--python', script_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0 and os.path.exists('duck.stl'):
            logger.info(f"✅ STL generated successfully for '{object_name}'")
            return True
        else:
            logger.error(f"❌ Blender script failed for '{object_name}'")
            if result.stderr:
                logger.debug(f"stderr: {result.stderr[-500:]}")
            return False

    except subprocess.TimeoutExpired:
        logger.error(f"⏰ Blender script timed out for '{object_name}'")
        return False
    except FileNotFoundError:
        logger.error("❌ Blender not found. Please install Blender and add to PATH.")
        return False
    finally:
        try:
            os.unlink(script_path)
        except:
            pass

def render_stl_to_image(output_image: str = 'render.png') -> bool:
    """Render STL file to image using Blender."""
    logger.info(f"📷 Rendering STL to image: {output_image}")

    if not os.path.exists('duck.stl'):
        logger.error("❌ duck.stl not found")
        return False

    blender_expr = f"""
import bpy

# Clear default objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import STL
bpy.ops.import_mesh.stl(filepath='duck.stl')

# Get the imported object
obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

# Center the object
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
obj.location = (0, 0, 0)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
light = bpy.context.active_object
light.data.energy = 3

# Position camera
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)

# Set camera as active
bpy.context.scene.camera = camera

# Set render settings
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 600
bpy.context.scene.render.filepath = '{output_image}'

# Render
bpy.ops.render.render(write_still=True)
"""

    try:
        cmd = ['blender', '--background', '--python-expr', blender_expr]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0 and os.path.exists(output_image):
            logger.info(f"✅ Render completed: {output_image}")
            return True
        else:
            logger.error(f"❌ Rendering failed")
            return False

    except subprocess.TimeoutExpired:
        logger.error("⏰ Rendering timed out")
        return False
    except FileNotFoundError:
        logger.error("❌ Blender not found")
        return False

def save_to_database(conn, object_name: str, description: str, code: str,
                     image_path: Optional[str]):
    """Save generated model to database."""
    cursor = conn.cursor()

    # Read image as binary if available
    image_blob = None
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_blob = f.read()

    cursor.execute('''
        INSERT OR REPLACE INTO models (object, description, code, image)
        VALUES (?, ?, ?, ?)
    ''', (object_name, description, code, image_blob))

    conn.commit()
    logger.info(f"💾 Saved '{object_name}' to database")

def upload_to_huggingface(conn, batch_count: int):
    """Upload batch to HuggingFace dataset."""
    try:
        logger.info(f"📤 Uploading batch {batch_count} to HuggingFace: {HF_REPO}")

        # Export database
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM models LIMIT ? OFFSET ?', (BATCH_SIZE, (batch_count - 1) * BATCH_SIZE))
        rows = cursor.fetchall()

        # Create temporary directory for export
        export_dir = f'export_batch_{batch_count}'
        os.makedirs(export_dir, exist_ok=True)

        # Save data
        for i, row in enumerate(rows):
            obj_name, desc, code, image = row

            # Save code
            if code:
                with open(f'{export_dir}/{obj_name.replace(" ", "_")}_code.py', 'w') as f:
                    f.write(code)

            # Save image
            if image:
                with open(f'{export_dir}/{obj_name.replace(" ", "_")}_render.png', 'wb') as f:
                    f.write(image)

        # Upload using huggingface-cli
        cmd = [
            'huggingface-cli', 'upload',
            HF_REPO,
            export_dir,
            '--repo-type=dataset'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logger.info(f"✅ Successfully uploaded batch {batch_count} to HuggingFace")
            return True
        else:
            logger.error(f"❌ HuggingFace upload failed: {result.stderr}")
            return False

    except Exception as e:
        logger.error(f"Error uploading to HuggingFace: {e}")
        return False

def check_already_processed(conn, object_name: str) -> bool:
    """Check if object already exists in database."""
    cursor = conn.cursor()
    cursor.execute('SELECT code, image FROM models WHERE object = ?', (object_name,))
    result = cursor.fetchone()
    # Only skip if both code and image exist
    return result is not None and result[0] is not None and result[1] is not None

def process_entity(client, conn, entity: Dict, batch_count: int) -> bool:
    """Process a single entity with retry logic."""
    object_name = entity['object']
    description = entity['description']

    # Check if already processed successfully
    if check_already_processed(conn, object_name):
        logger.info(f"⏭️  Skipping '{object_name}' - already processed successfully")
        return True

    logger.info(f"\n{'='*60}")
    logger.info(f"🎯 Processing: {object_name}")
    logger.info(f"{'='*60}")

    for attempt in range(1, MAX_RETRIES + 1):
        logger.info(f"Attempt {attempt}/{MAX_RETRIES}")

        # Generate code
        code = generate_blender_code(client, object_name, description)
        if not code:
            logger.warning(f"Failed to generate code, attempt {attempt}")
            continue

        # Run Blender script
        if not run_blender_script(code, object_name):
            logger.warning(f"Failed to run Blender script, attempt {attempt}")
            continue

        # Render image
        if not render_stl_to_image('render.png'):
            logger.warning(f"Failed to render image, attempt {attempt}")
            continue

        # Success!
        save_to_database(conn, object_name, description, code, 'render.png')

        # Cleanup
        try:
            os.unlink('duck.stl')
            os.unlink('render.png')
        except:
            pass

        return True

    # All attempts failed
    logger.error(f"❌ Failed to process '{object_name}' after {MAX_RETRIES} attempts")
    save_to_database(conn, object_name, description, code or "# Failed to generate", None)
    return False

def main():
    """Main function."""
    try:
        logger.info("🚀 Starting 3D model generation pipeline")

        # Setup
        conn = setup_database()
        client = setup_bedrock_client()

        # Load entities (limit to 10 for test batch)
        entities = load_entities('entities.json', limit=10)
        logger.info(f"📋 Loaded {len(entities)} entities (test batch)")

        # Process entities
        processed_count = 0
        success_count = 0

        for i, entity in enumerate(entities):
            success = process_entity(client, conn, entity, i // BATCH_SIZE)
            processed_count += 1
            if success:
                success_count += 1

            # Upload to HuggingFace after every BATCH_SIZE objects
            if processed_count % BATCH_SIZE == 0:
                batch_num = processed_count // BATCH_SIZE
                upload_to_huggingface(conn, batch_num)

        # Final upload if there are remaining items
        if processed_count % BATCH_SIZE != 0:
            batch_num = (processed_count // BATCH_SIZE) + 1
            upload_to_huggingface(conn, batch_num)

        # Summary
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Pipeline completed!")
        logger.info(f"📊 Processed: {processed_count}")
        logger.info(f"✅ Successful: {success_count}")
        logger.info(f"❌ Failed: {processed_count - success_count}")
        logger.info(f"💾 Database: {DB_FILE}")
        logger.info(f"{'='*60}")

        conn.close()

    except KeyboardInterrupt:
        logger.info("\n⏸️  Pipeline interrupted by user")
        if conn:
            conn.close()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
