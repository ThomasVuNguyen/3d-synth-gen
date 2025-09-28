#!/usr/bin/env python3
"""
Sample rendering script that:
1. Picks a random object from generated_scripts.json
2. Executes the Blender script to generate the STL
3. Renders the STL to an image
4. Displays the image in terminal

Usage:
    python render.py                    # Random object
    python render.py "abs chair"        # Specific object
    python render.py --list             # List available objects
"""

import json
import random
import subprocess
import sys
import os
import tempfile
import argparse

def load_generated_scripts():
    """Load the generated scripts from JSON file."""
    try:
        with open('generated_scripts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: generated_scripts.json not found. Run generate-dataset.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON in generated_scripts.json")
        sys.exit(1)

def extract_script_code(output_text):
    """Extract Python code from the output text (removes markdown formatting)."""
    lines = output_text.split('\n')
    code_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith('```python'):
            in_code_block = True
            continue
        elif line.strip() == '```' and in_code_block:
            in_code_block = False
            continue
        elif in_code_block:
            code_lines.append(line)

    return '\n'.join(code_lines)

def run_blender_script(script_code, object_name):
    """Run the Blender script to generate STL."""
    print(f"🎨 Generating 3D model for: {object_name}")

    # Create temporary Python script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script_code)
        script_path = f.name

    try:
        # Run Blender with the script
        cmd = ['blender', '--background', '--python', script_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("✅ STL generation completed successfully")
            return True
        else:
            print(f"❌ Blender script failed:")
            print(f"   stdout: {result.stdout[-200:] if result.stdout else 'None'}")
            print(f"   stderr: {result.stderr[-200:] if result.stderr else 'None'}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Blender script timed out (60s limit)")
        return False
    except FileNotFoundError:
        print("❌ Error: Blender not found. Please install Blender and add it to PATH.")
        return False
    finally:
        # Clean up temporary script file
        try:
            os.unlink(script_path)
        except:
            pass

def render_stl_to_image(output_image='render.png'):
    """Render STL file to image using Blender."""
    print(f"📷 Rendering STL to image: {output_image}")

    if not os.path.exists('duck.stl'):
        print("❌ Error: duck.stl not found")
        return False

    # Blender command to import STL and render
    blender_expr = f"""
import bpy
import bmesh

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
            print(f"✅ Render completed: {output_image}")
            return True
        else:
            print(f"❌ Rendering failed:")
            print(f"   Return code: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[-300:]}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Rendering timed out (120s limit)")
        return False
    except FileNotFoundError:
        print("❌ Error: Blender not found")
        return False

def display_image(image_path):
    """Display image in terminal using chafa if available."""
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return

    print(f"🖼️  Displaying {image_path}:")

    # Try to use chafa for terminal display
    try:
        subprocess.run(['chafa', '--size', '80x24', image_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📝 chafa not available. Install with: sudo apt install chafa")
        print(f"   Image saved as: {image_path}")

def main():
    parser = argparse.ArgumentParser(description="Render a random 3D object from generated scripts")
    parser.add_argument('object_name', nargs='?', help='Specific object to render')
    parser.add_argument('--list', action='store_true', help='List available objects')
    parser.add_argument('--output', default='render.png', help='Output image filename')

    args = parser.parse_args()

    # Load generated scripts
    scripts = load_generated_scripts()

    if args.list:
        print("📋 Available objects:")
        for script in scripts:
            print(f"   • {script['input']}")
        return

    # Select object
    if args.object_name:
        # Find specific object
        selected_script = None
        for script in scripts:
            if script['input'] == args.object_name:
                selected_script = script
                break

        if not selected_script:
            print(f"❌ Object '{args.object_name}' not found")
            print("💡 Use --list to see available objects")
            return
    else:
        # Pick random object
        selected_script = random.choice(scripts)

    object_name = selected_script['input']
    script_output = selected_script['output']

    print(f"🎲 Selected object: {object_name}")

    # Extract and run script
    script_code = extract_script_code(script_output)
    if not script_code.strip():
        print("❌ No valid Python code found in script output")
        return

    # Generate STL
    if not run_blender_script(script_code, object_name):
        return

    # Render image
    if not render_stl_to_image(args.output):
        return

    # Display image
    display_image(args.output)

    print(f"\n✅ Rendering complete for: {object_name}")
    print(f"📁 Files created:")
    print(f"   • duck.stl (3D model)")
    print(f"   • {args.output} (rendered image)")

if __name__ == "__main__":
    main()