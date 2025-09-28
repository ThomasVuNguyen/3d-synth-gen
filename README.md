# 3D Object Generator

Generate comprehensive lists of 3D object names for synthetic file generation and create Blender Python scripts using AWS Bedrock.

## Usage

### Generate Object List
```bash
python generate-entity.py
```

Generates `objects.txt` containing thousands of 3D object names suitable for synthetic 3D file generation.

### Generate Blender Scripts
```bash
pip install -r requirements.txt
python generate-dataset.py
```

Uses AWS Bedrock Sonnet 4 to generate Blender Python scripts for the first 3 objects from `objects.txt`. Results are saved to `generated_scripts.json`.

## Output

The script produces a sorted list of unique object names including:
- Furniture (chairs, tables, beds, etc.)
- Vehicles (cars, trucks, boats, aircraft)  
- Tools (hand tools, power tools)
- Electronics (computers, phones, cameras)
- Kitchen items (cookware, utensils, appliances)
- Household items (lamps, mirrors, containers)
- Materials, colors, sizes, and style variations

Perfect for generating diverse 3D model datasets.
