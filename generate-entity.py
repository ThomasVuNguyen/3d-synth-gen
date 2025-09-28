#!/usr/bin/env python3
"""
Generate 50,000+ 3D objects through systematic expansion.
"""

def generate_object_list():
    """Generate a comprehensive list of 50,000+ 3D object names."""
    
    # Read from existing objects.txt if available
    try:
        with open('objects.txt', 'r') as f:
            objects = [line.strip() for line in f if line.strip()]
        if len(objects) >= 50000:
            return objects
    except FileNotFoundError:
        pass
    
    # If file doesn't exist or has fewer than 50k objects, generate new list
    all_objects = set()
    
    # Massively expanded base categories
    furniture = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'bench', 'stool', 
        'dresser', 'nightstand', 'wardrobe', 'bookcase', 'credenza', 'ottoman', 'armchair', 
        'recliner', 'loveseat', 'sectional', 'futon', 'accent chair', 'bar stool', 
        'counter stool', 'piano bench', 'park bench', 'dining chair', 'office chair', 
        'rocking chair', 'folding chair', 'swivel chair', 'coffee table', 'dining table', 
        'end table', 'side table', 'console table', 'conference table', 'kitchen table', 
        'picnic table', 'drafting table', 'single bed', 'twin bed', 'full bed', 
        'queen bed', 'king bed', 'daybed', 'bunk bed', 'loft bed', 'murphy bed',
        'platform bed', 'canopy bed', 'sleigh bed', 'poster bed', 'panel bed',
        'storage bed', 'trundle bed', 'sofa bed', 'captain bed', 'race car bed'
    ]
    
    vehicles = [
        'car', 'sedan', 'hatchback', 'coupe', 'convertible', 'wagon', 'suv', 'crossover',
        'minivan', 'pickup truck', 'sports car', 'luxury car', 'police car', 'taxi',
        'ambulance', 'fire truck', 'limousine', 'race car', 'motorcycle', 'scooter',
        'bicycle', 'truck', 'delivery truck', 'dump truck', 'garbage truck', 'tow truck',
        'bus', 'school bus', 'city bus', 'tour bus', 'airplane', 'jet', 'helicopter',
        'boat', 'yacht', 'sailboat', 'motorboat', 'speedboat', 'canoe', 'kayak',
        'tricycle', 'unicycle', 'mountain bike', 'road bike', 'hybrid bike', 'bmx bike',
        'electric bike', 'tandem bike', 'folding bike', 'cargo bike', 'cruiser bike',
        'atv', 'utv', 'snowmobile', 'jet ski', 'personal watercraft', 'pontoon boat',
        'fishing boat', 'cabin cruiser', 'bowrider', 'ski boat', 'wake boat',
        'catamaran', 'trimaran', 'houseboat', 'tugboat', 'barge', 'ferry'
    ]
    
    tools = [
        'hammer', 'screwdriver', 'wrench', 'pliers', 'saw', 'drill', 'chisel',
        'file', 'sandpaper', 'level', 'measuring tape', 'ruler', 'square',
        'crowbar', 'axe', 'pickaxe', 'shovel', 'rake', 'hoe', 'spade',
        'circular saw', 'jigsaw', 'angle grinder', 'belt sander', 'router',
        'socket wrench', 'allen wrench', 'pipe wrench', 'needle nose pliers',
        'claw hammer', 'ball peen hammer', 'sledge hammer', 'framing hammer',
        'dead blow hammer', 'rubber mallet', 'wooden mallet', 'combination wrench',
        'box wrench', 'open end wrench', 'torque wrench', 'basin wrench',
        'strap wrench', 'chain wrench', 'adjustable wrench', 'ratcheting wrench',
        'slip joint pliers', 'locking pliers', 'wire cutters', 'diagonal cutters',
        'lineman pliers', 'fence pliers', 'crimping pliers', 'welding pliers'
    ]
    
    electronics = [
        'computer', 'laptop', 'desktop', 'tablet', 'smartphone', 'phone', 'camera',
        'television', 'monitor', 'speaker', 'headphones', 'microphone', 'radio',
        'stereo', 'amplifier', 'receiver', 'turntable', 'cd player', 'dvd player',
        'projector', 'printer', 'scanner', 'router', 'modem', 'keyboard', 'mouse',
        'gaming console', 'handheld console', 'vr headset', 'smartwatch', 'fitness tracker',
        'bluetooth speaker', 'soundbar', 'subwoofer', 'bookshelf speaker', 'floor speaker',
        'wireless headphones', 'earbuds', 'gaming headset', 'webcam', 'action camera',
        'security camera', 'doorbell camera', 'dash cam', 'drone', 'rc car',
        'smart tv', 'streaming device', 'media player', 'game controller', 'joystick'
    ]
    
    kitchen = [
        'pot', 'pan', 'skillet', 'saucepan', 'stockpot', 'dutch oven', 'wok',
        'knife', 'chef knife', 'paring knife', 'bread knife', 'fork', 'spoon',
        'spatula', 'whisk', 'ladle', 'tongs', 'peeler', 'grater', 'can opener',
        'bottle opener', 'corkscrew', 'measuring cup', 'mixing bowl', 'cutting board',
        'colander', 'strainer', 'timer', 'thermometer', 'scale', 'blender',
        'food processor', 'mixer', 'toaster', 'coffee maker', 'kettle', 'teapot',
        'pressure cooker', 'slow cooker', 'rice cooker', 'steamer', 'double boiler',
        'roasting pan', 'baking dish', 'casserole dish', 'grill pan', 'crepe pan',
        'omelet pan', 'paella pan', 'tagine', 'griddle', 'carving knife',
        'utility knife', 'boning knife', 'fillet knife', 'cleaver', 'steak knife'
    ]
    
    household = [
        'lamp', 'mirror', 'vase', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle',
        'clock', 'picture', 'frame', 'box', 'basket', 'bin', 'container', 'jar',
        'bag', 'purse', 'wallet', 'case', 'pillow', 'cushion', 'blanket', 'towel',
        'curtain', 'blind', 'rug', 'carpet', 'doormat', 'umbrella', 'candle',
        'candlestick', 'ashtray', 'coaster', 'tissue box', 'trash can', 'hamper',
        'laundry basket', 'storage basket', 'picnic basket', 'fruit basket',
        'bread basket', 'wastepaper basket', 'toy box', 'storage box', 'jewelry box',
        'tool box', 'lunch box', 'music box', 'recycling bin', 'compost bin'
    ]
    
    appliances = [
        'refrigerator', 'oven', 'microwave', 'dishwasher', 'washing machine',
        'dryer', 'air conditioner', 'heater', 'vacuum cleaner', 'iron',
        'french door refrigerator', 'side by side refrigerator', 'top freezer refrigerator',
        'bottom freezer refrigerator', 'mini fridge', 'wine refrigerator', 'beverage cooler',
        'ice maker', 'water dispenser', 'gas oven', 'electric oven', 'convection oven',
        'toaster oven', 'countertop oven', 'steam oven', 'combination oven', 'pizza oven'
    ]
    
    sports = [
        'baseball', 'basketball', 'football', 'soccer ball', 'tennis ball',
        'golf ball', 'volleyball', 'hockey puck', 'bat', 'racket', 'club',
        'glove', 'helmet', 'skates', 'skis', 'snowboard', 'surfboard',
        'ping pong ball', 'ping pong paddle', 'badminton racket', 'squash racket',
        'lacrosse stick', 'hockey stick', 'pool cue', 'dart', 'dartboard',
        'bowling ball', 'bowling pin', 'billiard ball', 'boxing gloves', 'punching bag',
        'exercise bike', 'treadmill', 'elliptical', 'rowing machine', 'weight bench'
    ]
    
    musical = [
        'guitar', 'piano', 'violin', 'drums', 'trumpet', 'saxophone', 'flute',
        'clarinet', 'trombone', 'cello', 'bass', 'keyboard', 'harmonica',
        'acoustic guitar', 'electric guitar', 'bass guitar', 'classical guitar',
        'banjo', 'mandolin', 'ukulele', 'harp', 'accordion', 'bagpipes',
        'drum kit', 'snare drum', 'bass drum', 'bongos', 'conga drums',
        'cymbals', 'xylophone', 'marimba', 'vibraphone', 'synthesizer'
    ]
    
    office = [
        'pen', 'pencil', 'marker', 'ruler', 'calculator', 'stapler', 'scissors',
        'notebook', 'binder', 'folder', 'clipboard', 'whiteboard', 'calendar',
        'ballpoint pen', 'gel pen', 'felt tip pen', 'fountain pen', 'mechanical pencil',
        'colored pencil', 'permanent marker', 'dry erase marker', 'highlighter',
        'eraser', 'paper clips', 'binder clips', 'pushpins', 'thumbtacks'
    ]
    
    # NEW CATEGORIES FOR 50K EXPANSION
    
    clothing = [
        'shirt', 'pants', 'dress', 'skirt', 'jacket', 'coat', 'sweater', 'hoodie',
        'jeans', 'shorts', 'blouse', 'suit', 'tie', 'scarf', 'hat', 'cap',
        'shoes', 'boots', 'sneakers', 'sandals', 'heels', 'flats', 'loafers',
        'socks', 'underwear', 'bra', 'belt', 'gloves', 'mittens', 'vest'
    ]
    
    jewelry = [
        'necklace', 'bracelet', 'ring', 'earrings', 'watch', 'pendant', 'chain',
        'brooch', 'pin', 'cufflinks', 'tie clip', 'anklet', 'charm', 'locket',
        'engagement ring', 'wedding ring', 'class ring', 'signet ring', 'cocktail ring'
    ]
    
    toys = [
        'doll', 'action figure', 'toy car', 'toy truck', 'toy plane', 'toy train',
        'blocks', 'lego', 'puzzle', 'board game', 'card game', 'chess set',
        'checkers', 'dominos', 'yo yo', 'kite', 'frisbee', 'ball', 'balloon',
        'stuffed animal', 'teddy bear', 'rocking horse', 'tricycle', 'scooter'
    ]
    
    medical = [
        'stethoscope', 'thermometer', 'blood pressure cuff', 'syringe', 'bandage',
        'gauze', 'cast', 'crutch', 'wheelchair', 'walker', 'cane', 'splint',
        'ice pack', 'heating pad', 'pill bottle', 'medicine bottle', 'inhaler',
        'nebulizer', 'oxygen tank', 'defibrillator', 'x ray machine', 'mri machine'
    ]
    
    garden = [
        'flower pot', 'planter', 'watering can', 'garden hose', 'sprinkler',
        'lawn mower', 'leaf blower', 'hedge trimmer', 'pruning shears', 'garden rake',
        'garden shovel', 'trowel', 'wheelbarrow', 'garden cart', 'compost bin',
        'greenhouse', 'gazebo', 'pergola', 'arbor', 'trellis', 'fence', 'gate'
    ]
    
    art_supplies = [
        'paintbrush', 'paint', 'canvas', 'easel', 'palette', 'palette knife',
        'pencil', 'charcoal', 'pastel', 'crayon', 'marker', 'pen', 'ink',
        'sketchbook', 'drawing pad', 'watercolor', 'acrylic paint', 'oil paint',
        'spray paint', 'paint roller', 'paint tray', 'masking tape', 'drop cloth'
    ]
    
    # Add all categories
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
    all_objects.update(clothing)
    all_objects.update(jewelry)
    all_objects.update(toys)
    all_objects.update(medical)
    all_objects.update(garden)
    all_objects.update(art_supplies)
    
    # Massively expanded modifiers for 50K target
    materials = [
        'wooden', 'oak', 'pine', 'maple', 'cherry', 'walnut', 'mahogany', 'teak', 'cedar',
        'birch', 'ash', 'poplar', 'bamboo', 'cork', 'plywood', 'mdf', 'particle board',
        'metal', 'steel', 'stainless steel', 'carbon steel', 'aluminum', 'copper', 'brass', 
        'bronze', 'iron', 'cast iron', 'wrought iron', 'titanium', 'chrome', 'nickel',
        'zinc', 'tin', 'lead', 'silver', 'gold', 'platinum', 'galvanized', 'powder coated',
        'plastic', 'acrylic', 'polycarbonate', 'abs', 'pvc', 'polyethylene', 'polypropylene',
        'nylon', 'polyester', 'vinyl', 'fiberglass', 'carbon fiber', 'kevlar', 'silicone',
        'rubber', 'natural rubber', 'synthetic rubber', 'foam rubber', 'neoprene',
        'glass', 'tempered glass', 'laminated glass', 'safety glass', 'frosted glass',
        'tinted glass', 'crystal', 'ceramic', 'porcelain', 'earthenware', 'stoneware',
        'fabric', 'cotton', 'wool', 'silk', 'linen', 'canvas', 'denim', 'leather',
        'genuine leather', 'faux leather', 'suede', 'microfiber', 'velvet', 'corduroy',
        'stone', 'marble', 'granite', 'slate', 'limestone', 'sandstone', 'travertine',
        'concrete', 'brick', 'clay', 'terra cotta', 'wicker', 'rattan', 'cane', 'jute'
    ]
    
    colors = [
        'red', 'crimson', 'scarlet', 'burgundy', 'maroon', 'cherry', 'rose', 'pink',
        'hot pink', 'magenta', 'fuchsia', 'coral', 'salmon', 'peach', 'orange',
        'tangerine', 'amber', 'yellow', 'golden', 'lemon', 'lime', 'chartreuse',
        'green', 'forest green', 'emerald', 'sage', 'olive', 'mint', 'teal',
        'turquoise', 'aqua', 'cyan', 'blue', 'navy', 'royal blue', 'sky blue',
        'powder blue', 'periwinkle', 'indigo', 'violet', 'purple', 'lavender',
        'plum', 'grape', 'black', 'charcoal', 'gray', 'grey', 'silver', 'white',
        'ivory', 'cream', 'beige', 'tan', 'brown', 'chocolate', 'coffee', 'espresso'
    ]
    
    sizes = [
        'mini', 'micro', 'tiny', 'small', 'compact', 'petite', 'medium', 'standard',
        'regular', 'large', 'big', 'extra large', 'xl', 'xxl', 'oversized', 'giant',
        'jumbo', 'massive', 'huge', 'enormous', 'pocket', 'travel', 'portable',
        'desktop', 'tabletop', 'countertop', 'floor', 'standing', 'wall', 'ceiling',
        'commercial', 'industrial', 'professional', 'residential', 'home', 'office',
        'studio', 'deluxe', 'premium', 'luxury', 'economy', 'basic', 'entry level'
    ]
    
    styles = [
        'modern', 'contemporary', 'traditional', 'classic', 'vintage', 'antique',
        'retro', 'mid century', 'art deco', 'art nouveau', 'craftsman', 'mission',
        'shaker', 'colonial', 'victorian', 'georgian', 'federal', 'empire',
        'neoclassical', 'baroque', 'rococo', 'gothic', 'renaissance', 'rustic',
        'farmhouse', 'country', 'cottage', 'shabby chic', 'industrial', 'urban',
        'minimalist', 'scandinavian', 'danish', 'swedish', 'norwegian', 'finnish',
        'mediterranean', 'tuscan', 'spanish', 'moroccan', 'asian', 'japanese',
        'chinese', 'korean', 'indian', 'french', 'english', 'american', 'western',
        'southwestern', 'tropical', 'coastal', 'nautical', 'bohemian', 'eclectic'
    ]
    
    # Expanded modifier sets for 50K
    modifiers = [
        'adjustable', 'foldable', 'stackable', 'portable', 'electric', 'manual', 
        'automatic', 'digital', 'analog', 'wireless', 'bluetooth', 'smart',
        'programmable', 'rechargeable', 'battery powered', 'solar powered',
        'waterproof', 'fireproof', 'rustproof', 'shatterproof', 'scratch resistant'
    ]
    
    conditions = [
        'new', 'used', 'vintage', 'antique', 'refurbished', 'restored', 'custom',
        'handmade', 'artisan', 'designer', 'luxury', 'premium', 'imported',
        'damaged', 'broken', 'cracked', 'chipped', 'scratched', 'dented'
    ]
    
    rooms = [
        'living room', 'bedroom', 'dining room', 'kitchen', 'bathroom', 'office',
        'family room', 'den', 'study', 'nursery', 'guest room', 'master bedroom',
        'basement', 'attic', 'garage', 'laundry room', 'mudroom', 'pantry',
        'closet', 'hallway', 'entryway', 'foyer', 'sunroom', 'conservatory'
    ]
    
    # Expanded key objects for more combinations
    key_objects = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'lamp',
        'mirror', 'vase', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle',
        'pot', 'pan', 'knife', 'fork', 'spoon', 'clock', 'picture', 'frame',
        'box', 'basket', 'bin', 'container', 'jar', 'bag', 'purse', 'wallet',
        'pillow', 'cushion', 'blanket', 'towel', 'curtain', 'rug', 'carpet'
    ]
    
    # Generate massive combinations to reach 50K+
    print("Generating material combinations...")
    for obj in key_objects:
        for material in materials:
            all_objects.add(f"{material} {obj}")
    
    print("Generating color combinations...")
    for obj in key_objects:
        for color in colors:
            all_objects.add(f"{color} {obj}")
    
    print("Generating size combinations...")
    for obj in key_objects:
        for size in sizes:
            all_objects.add(f"{size} {obj}")
    
    print("Generating style combinations...")
    for obj in key_objects:
        for style in styles:
            all_objects.add(f"{style} {obj}")
    
    print("Generating modifier combinations...")
    for modifier in modifiers:
        for obj in key_objects:
            all_objects.add(f"{modifier} {obj}")
    
    print("Generating condition combinations...")
    for condition in conditions:
        for obj in key_objects:
            all_objects.add(f"{condition} {obj}")
    
    print("Generating room combinations...")
    for room in rooms:
        for obj in key_objects:
            all_objects.add(f"{room} {obj}")
    
    # Add cross-combinations for even more variety to reach 50K
    print("Generating cross-combinations...")
    for material in materials[:25]:  # Top 25 materials
        for color in colors[:25]:    # Top 25 colors
            for obj in key_objects[:20]:  # Top 20 objects
                all_objects.add(f"{material} {color} {obj}")
    
    for size in sizes[:20]:  # Top 20 sizes
        for style in styles[:20]:  # Top 20 styles
            for obj in key_objects[:15]:  # Top 15 objects
                all_objects.add(f"{size} {style} {obj}")
    
    # Triple combinations for maximum expansion
    print("Generating triple combinations...")
    for material in materials[:15]:  # Top 15 materials
        for size in sizes[:15]:      # Top 15 sizes
            for obj in key_objects[:10]:  # Top 10 objects
                all_objects.add(f"{material} {size} {obj}")
    
    for color in colors[:15]:        # Top 15 colors
        for condition in conditions[:10]:  # Top 10 conditions
            for obj in key_objects[:10]:   # Top 10 objects
                all_objects.add(f"{color} {condition} {obj}")
    
    # Quadruple combinations for maximum variety
    print("Generating quadruple combinations...")
    for material in materials[:10]:  # Top 10 materials
        for color in colors[:10]:    # Top 10 colors
            for size in sizes[:8]:   # Top 8 sizes
                for obj in key_objects[:8]:  # Top 8 objects
                    all_objects.add(f"{material} {color} {size} {obj}")
    
    # Room + style + object combinations
    print("Generating room-style combinations...")
    for room in rooms[:20]:         # Top 20 rooms
        for style in styles[:20]:   # Top 20 styles
            for obj in key_objects[:15]:  # Top 15 objects
                all_objects.add(f"{room} {style} {obj}")
    
    # Material + condition + object combinations
    print("Generating material-condition combinations...")
    for material in materials[:20]:   # Top 20 materials
        for condition in conditions:  # All conditions
            for obj in key_objects[:15]:  # Top 15 objects
                all_objects.add(f"{material} {condition} {obj}")
    
    print(f"Generated {len(all_objects)} unique objects")
    return sorted(list(all_objects))

def main():
    objects = generate_object_list()
    
    # Write to file
    with open('objects.txt', 'w') as f:
        for obj in objects:
            f.write(obj + '\n')
    
    print(f"Generated {len(objects)} objects")
    print(f"Saved to objects.txt")
    
    if len(objects) >= 50000:
        print("✅ Successfully reached 50,000+ objects!")
    elif len(objects) >= 10000:
        print(f"✅ Generated {len(objects)} objects (10K+ target met)")
    else:
        print(f"📊 Generated {len(objects)} objects")

if __name__ == "__main__":
    main()