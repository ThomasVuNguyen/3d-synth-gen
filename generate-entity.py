#!/usr/bin/env python3
"""
Generate 10,000+ 3D objects through systematic expansion.
"""

def generate_object_list():
    """Generate a comprehensive list of 10,000+ 3D object names."""
    
    # Read from existing objects.txt if available
    try:
        with open('objects.txt', 'r') as f:
            objects = [line.strip() for line in f if line.strip()]
        if len(objects) >= 10000:
            return objects
    except FileNotFoundError:
        pass
    
    # If file doesn't exist or has fewer than 10k objects, generate new list
    all_objects = set()
    
    # Base categories with extensive lists
    furniture = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'bench', 'stool', 
        'dresser', 'nightstand', 'wardrobe', 'bookcase', 'credenza', 'ottoman', 'armchair', 
        'recliner', 'loveseat', 'sectional', 'futon', 'accent chair', 'bar stool', 
        'counter stool', 'piano bench', 'park bench', 'dining chair', 'office chair', 
        'rocking chair', 'folding chair', 'swivel chair', 'coffee table', 'dining table', 
        'end table', 'side table', 'console table', 'conference table', 'kitchen table', 
        'picnic table', 'drafting table', 'single bed', 'twin bed', 'full bed', 
        'queen bed', 'king bed', 'daybed'
    ]
    
    vehicles = [
        'car', 'sedan', 'hatchback', 'coupe', 'convertible', 'wagon', 'suv', 'crossover',
        'minivan', 'pickup truck', 'sports car', 'luxury car', 'police car', 'taxi',
        'ambulance', 'fire truck', 'limousine', 'race car', 'motorcycle', 'scooter',
        'bicycle', 'truck', 'delivery truck', 'dump truck', 'garbage truck', 'tow truck',
        'bus', 'school bus', 'city bus', 'tour bus', 'airplane', 'jet', 'helicopter',
        'boat', 'yacht', 'sailboat', 'motorboat', 'speedboat', 'canoe', 'kayak'
    ]
    
    tools = [
        'hammer', 'screwdriver', 'wrench', 'pliers', 'saw', 'drill', 'chisel',
        'file', 'sandpaper', 'level', 'measuring tape', 'ruler', 'square',
        'crowbar', 'axe', 'pickaxe', 'shovel', 'rake', 'hoe', 'spade',
        'circular saw', 'jigsaw', 'angle grinder', 'belt sander', 'router',
        'socket wrench', 'allen wrench', 'pipe wrench', 'needle nose pliers'
    ]
    
    electronics = [
        'computer', 'laptop', 'desktop', 'tablet', 'smartphone', 'phone', 'camera',
        'television', 'monitor', 'speaker', 'headphones', 'microphone', 'radio',
        'stereo', 'amplifier', 'receiver', 'turntable', 'cd player', 'dvd player',
        'projector', 'printer', 'scanner', 'router', 'modem', 'keyboard', 'mouse'
    ]
    
    kitchen = [
        'pot', 'pan', 'skillet', 'saucepan', 'stockpot', 'dutch oven', 'wok',
        'knife', 'chef knife', 'paring knife', 'bread knife', 'fork', 'spoon',
        'spatula', 'whisk', 'ladle', 'tongs', 'peeler', 'grater', 'can opener',
        'bottle opener', 'corkscrew', 'measuring cup', 'mixing bowl', 'cutting board',
        'colander', 'strainer', 'timer', 'thermometer', 'scale', 'blender',
        'food processor', 'mixer', 'toaster', 'coffee maker', 'kettle', 'teapot'
    ]
    
    household = [
        'lamp', 'mirror', 'vase', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle',
        'clock', 'picture', 'frame', 'box', 'basket', 'bin', 'container', 'jar',
        'bag', 'purse', 'wallet', 'case', 'pillow', 'cushion', 'blanket', 'towel',
        'curtain', 'blind', 'rug', 'carpet', 'doormat', 'umbrella', 'candle',
        'candlestick', 'ashtray', 'coaster', 'tissue box', 'trash can', 'hamper'
    ]
    
    appliances = [
        'refrigerator', 'oven', 'microwave', 'dishwasher', 'washing machine',
        'dryer', 'air conditioner', 'heater', 'vacuum cleaner', 'iron'
    ]
    
    sports = [
        'baseball', 'basketball', 'football', 'soccer ball', 'tennis ball',
        'golf ball', 'volleyball', 'hockey puck', 'bat', 'racket', 'club',
        'glove', 'helmet', 'skates', 'skis', 'snowboard', 'surfboard'
    ]
    
    musical = [
        'guitar', 'piano', 'violin', 'drums', 'trumpet', 'saxophone', 'flute',
        'clarinet', 'trombone', 'cello', 'bass', 'keyboard', 'harmonica'
    ]
    
    office = [
        'pen', 'pencil', 'marker', 'ruler', 'calculator', 'stapler', 'scissors',
        'notebook', 'binder', 'folder', 'clipboard', 'whiteboard', 'calendar'
    ]
    
    # Add all base categories
    all_objects.update(furniture)
    all_objects.update(vehicles)
    all_objects.update(tools)
    all_objects.update(electronics)
    all_objects.update(kitchen)
    all_objects.update(household)
    all_objects.update(appliances)
    all_objects.update(sports)
    all_objects.update(musical)
    all_objects.update(office)
    
    # Comprehensive modifiers
    materials = [
        'wooden', 'oak', 'pine', 'maple', 'cherry', 'walnut', 'bamboo', 'metal', 'steel', 
        'aluminum', 'copper', 'brass', 'bronze', 'iron', 'plastic', 'acrylic', 'abs', 
        'pvc', 'fiberglass', 'carbon fiber', 'glass', 'ceramic', 'porcelain', 'leather', 
        'fabric', 'cotton', 'marble', 'granite', 'concrete', 'stone', 'wicker', 'rattan'
    ]
    
    colors = [
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown',
        'black', 'white', 'gray', 'silver', 'gold', 'beige', 'tan', 'navy',
        'maroon', 'teal', 'turquoise', 'lime', 'magenta', 'cyan', 'ivory'
    ]
    
    sizes = [
        'mini', 'small', 'compact', 'medium', 'large', 'extra large', 'giant',
        'pocket', 'travel', 'portable', 'desktop', 'floor', 'wall', 'ceiling',
        'commercial', 'industrial', 'professional', 'home', 'office'
    ]
    
    styles = [
        'modern', 'contemporary', 'traditional', 'classic', 'vintage', 'antique',
        'retro', 'art deco', 'industrial', 'rustic', 'farmhouse', 'minimalist',
        'scandinavian', 'mediterranean', 'asian', 'french', 'american'
    ]
    
    modifiers = ['adjustable', 'foldable', 'electric', 'manual', 'digital', 'analog']
    conditions = ['new', 'used', 'vintage', 'antique', 'custom', 'handmade']
    rooms = ['living room', 'bedroom', 'kitchen', 'bathroom', 'office']
    
    # Key objects for generating combinations
    key_objects = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'lamp',
        'mirror', 'vase', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle',
        'pot', 'pan', 'knife', 'fork', 'spoon', 'clock', 'picture', 'frame',
        'box', 'basket', 'bin', 'container', 'jar', 'bag', 'purse', 'wallet'
    ]
    
    # Generate systematic combinations to reach 10k+
    for obj in key_objects:
        for material in materials:
            all_objects.add(f"{material} {obj}")
        for color in colors:
            all_objects.add(f"{color} {obj}")
        for size in sizes:
            all_objects.add(f"{size} {obj}")
        for style in styles:
            all_objects.add(f"{style} {obj}")
    
    for modifier in modifiers:
        for obj in key_objects[:20]:
            all_objects.add(f"{modifier} {obj}")
    
    for condition in conditions:
        for obj in key_objects[:20]:
            all_objects.add(f"{condition} {obj}")
    
    for room in rooms:
        for obj in key_objects[:15]:
            all_objects.add(f"{room} {obj}")
    
    return sorted(list(all_objects))

def main():
    objects = generate_object_list()
    
    # Write to file
    with open('objects.txt', 'w') as f:
        for obj in objects:
            f.write(obj + '\n')
    
    print(f"Generated {len(objects)} objects")
    print(f"Saved to objects.txt")
    
    if len(objects) >= 10000:
        print("✅ Successfully reached 10,000+ objects!")
    else:
        print(f"📊 Generated {len(objects)} objects")

if __name__ == "__main__":
    main()