#!/usr/bin/env python3
"""
Generate a comprehensive list of 10,000 3D objects by expanding base objects
with variations in materials, sizes, styles, colors, and specific types.
"""

def generate_10k_objects():
    """Generate 10,000 3D object names through systematic expansion."""
    
    # Base objects from our curated list
    base_objects = [
        # Furniture & Seating
        'chair', 'table', 'sofa', 'bed', 'desk', 'shelf', 'cabinet', 'bench',
        'stool', 'armchair', 'recliner', 'loveseat', 'ottoman', 'bookcase',
        'dresser', 'nightstand', 'wardrobe', 'credenza', 'hutch', 'vanity',
        
        # Vehicles
        'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'airplane', 'boat',
        'helicopter', 'ship', 'train', 'scooter', 'van', 'ambulance', 'taxi',
        'jet', 'sailboat', 'yacht', 'canoe', 'kayak', 'submarine',
        
        # Kitchen Items
        'cup', 'mug', 'bowl', 'plate', 'glass', 'bottle', 'pot', 'pan',
        'knife', 'fork', 'spoon', 'kettle', 'toaster', 'blender', 'oven',
        'microwave', 'refrigerator', 'dishwasher', 'mixer', 'grater',
        
        # Tools & Equipment
        'hammer', 'screwdriver', 'wrench', 'drill', 'saw', 'scissors',
        'pliers', 'ladder', 'shovel', 'rake', 'axe', 'chisel', 'file',
        'clamp', 'vise', 'level', 'ruler', 'square', 'crowbar',
        
        # Electronics
        'computer', 'phone', 'camera', 'television', 'radio', 'speaker',
        'monitor', 'keyboard', 'mouse', 'tablet', 'laptop', 'printer',
        'scanner', 'projector', 'headphones', 'microphone',
        
        # Home Items
        'lamp', 'clock', 'mirror', 'vase', 'pillow', 'towel', 'blanket',
        'candle', 'basket', 'bucket', 'box', 'bag', 'suitcase', 'umbrella',
        'vacuum', 'broom', 'mop', 'iron', 'fan', 'heater',
        
        # Sports & Recreation
        'ball', 'bat', 'racket', 'club', 'helmet', 'skateboard', 'skis',
        'surfboard', 'bicycle', 'dumbbell', 'barbell', 'treadmill',
        
        # Musical Instruments
        'guitar', 'piano', 'drum', 'violin', 'trumpet', 'flute', 'saxophone',
        'clarinet', 'bass', 'keyboard', 'harmonica', 'accordion',
        
        # Food Items
        'apple', 'banana', 'orange', 'grape', 'strawberry', 'carrot',
        'potato', 'tomato', 'bread', 'cake', 'pizza', 'sandwich',
        
        # Containers & Storage
        'jar', 'can', 'barrel', 'crate', 'chest', 'trunk', 'bin',
        
        # Clothing & Accessories
        'shoe', 'boot', 'hat', 'cap', 'glove', 'belt', 'watch', 'ring',
        'necklace', 'earring', 'glasses', 'purse', 'wallet',
        
        # Building Elements
        'door', 'window', 'roof', 'chimney', 'fence', 'gate', 'stairs',
        
        # Nature
        'tree', 'flower', 'plant', 'leaf', 'branch', 'rock', 'stone'
    ]
    
    # Material variations
    materials = [
        'wooden', 'metal', 'plastic', 'glass', 'ceramic', 'fabric', 'leather',
        'rubber', 'concrete', 'stone', 'marble', 'granite', 'steel', 'iron',
        'aluminum', 'copper', 'brass', 'bronze', 'titanium', 'carbon fiber',
        'fiberglass', 'bamboo', 'wicker', 'rattan', 'vinyl', 'silicone',
        'porcelain', 'crystal', 'acrylic', 'plywood', 'hardwood', 'softwood',
        'oak', 'pine', 'maple', 'mahogany', 'teak', 'cedar', 'walnut',
        'chrome', 'stainless steel', 'cast iron', 'wrought iron'
    ]
    
    # Size variations
    sizes = [
        'mini', 'small', 'medium', 'large', 'extra large', 'giant', 'tiny',
        'compact', 'full size', 'oversized', 'pocket', 'desktop', 'floor',
        'wall mounted', 'portable', 'handheld', 'industrial', 'commercial',
        'residential', 'professional', 'standard', 'deluxe', 'economy'
    ]
    
    # Style variations
    styles = [
        'modern', 'vintage', 'antique', 'contemporary', 'traditional',
        'classic', 'retro', 'rustic', 'industrial', 'minimalist',
        'ornate', 'baroque', 'art deco', 'victorian', 'colonial',
        'scandinavian', 'mediterranean', 'asian', 'western', 'eastern',
        'urban', 'rural', 'military', 'nautical', 'aviation'
    ]
    
    # Colors
    colors = [
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
        'black', 'white', 'gray', 'brown', 'tan', 'beige', 'navy',
        'maroon', 'teal', 'turquoise', 'lime', 'olive', 'silver', 'gold'
    ]
    
    # Specific types and variations for major categories
    specific_furniture = [
        'dining chair', 'office chair', 'rocking chair', 'folding chair',
        'bar stool', 'counter stool', 'piano bench', 'park bench',
        'coffee table', 'dining table', 'end table', 'side table',
        'picnic table', 'pool table', 'ping pong table', 'conference table',
        'kitchen table', 'breakfast table', 'console table', 'accent table',
        'sectional sofa', 'sleeper sofa', 'loveseat', 'chaise lounge',
        'futon', 'daybed', 'bunk bed', 'murphy bed', 'platform bed',
        'canopy bed', 'sleigh bed', 'twin bed', 'queen bed', 'king bed',
        'single bed', 'double bed', 'sofa bed', 'rollaway bed',
        'computer desk', 'writing desk', 'standing desk', 'corner desk',
        'executive desk', 'student desk', 'drafting table', 'workbench'
    ]
    
    specific_vehicles = [
        'sedan', 'suv', 'pickup truck', 'convertible', 'coupe', 'hatchback',
        'station wagon', 'minivan', 'sports car', 'luxury car', 'economy car',
        'electric car', 'hybrid car', 'diesel truck', 'delivery truck',
        'garbage truck', 'fire truck', 'tow truck', 'dump truck', 'cement truck',
        'school bus', 'city bus', 'tour bus', 'charter bus', 'double decker bus',
        'racing motorcycle', 'touring motorcycle', 'dirt bike', 'scooter',
        'moped', 'mountain bike', 'road bike', 'bmx bike', 'electric bike',
        'cargo plane', 'passenger plane', 'fighter jet', 'private jet',
        'glider', 'seaplane', 'helicopter', 'cargo helicopter', 'rescue helicopter',
        'fishing boat', 'speed boat', 'cruise ship', 'cargo ship', 'tugboat',
        'ferry', 'catamaran', 'trimaran', 'yacht', 'sailboat', 'motorboat'
    ]
    
    specific_tools = [
        'claw hammer', 'ball peen hammer', 'sledge hammer', 'rubber mallet',
        'dead blow hammer', 'framing hammer', 'tack hammer', 'club hammer',
        'flat head screwdriver', 'phillips screwdriver', 'torx screwdriver',
        'electric screwdriver', 'precision screwdriver', 'stubby screwdriver',
        'combination wrench', 'socket wrench', 'pipe wrench', 'monkey wrench',
        'torque wrench', 'box wrench', 'open end wrench', 'ratcheting wrench',
        'cordless drill', 'hammer drill', 'impact drill', 'drill press',
        'hand drill', 'masonry drill', 'wood drill', 'metal drill',
        'hand saw', 'circular saw', 'jigsaw', 'reciprocating saw', 'band saw',
        'table saw', 'miter saw', 'chain saw', 'hack saw', 'coping saw'
    ]
    
    specific_electronics = [
        'desktop computer', 'laptop computer', 'tablet computer', 'all in one computer',
        'gaming computer', 'workstation', 'server', 'mini computer',
        'smartphone', 'flip phone', 'cordless phone', 'landline phone',
        'satellite phone', 'walkie talkie', 'two way radio', 'cb radio',
        'digital camera', 'film camera', 'instant camera', 'security camera',
        'action camera', 'drone camera', 'webcam', 'video camera',
        'lcd television', 'led television', 'plasma television', 'smart tv',
        'portable tv', 'projector tv', 'rear projection tv', 'crt television',
        'am radio', 'fm radio', 'shortwave radio', 'weather radio',
        'portable radio', 'clock radio', 'car radio', 'two way radio'
    ]
    
    # Professional and industrial equipment
    professional_equipment = [
        'oscilloscope', 'multimeter', 'function generator', 'power supply',
        'spectrum analyzer', 'signal generator', 'logic analyzer', 'voltmeter',
        'ammeter', 'ohmmeter', 'frequency counter', 'lcr meter', 'capacitance meter',
        'insulation tester', 'earth tester', 'clamp meter', 'phase meter',
        'welding machine', 'plasma cutter', 'angle grinder', 'bench grinder',
        'belt sander', 'orbital sander', 'palm sander', 'disc sander',
        'router table', 'jointer', 'planer', 'band saw', 'scroll saw',
        'lathe', 'milling machine', 'drill press', 'mortiser', 'shaper',
        'compressor', 'generator', 'pressure washer', 'shop vacuum',
        'dust collector', 'air filtration system', 'ventilation fan',
        'hydraulic jack', 'floor jack', 'bottle jack', 'scissor jack',
        'engine hoist', 'engine stand', 'transmission jack', 'axle stand',
        'tire changer', 'wheel balancer', 'brake lathe', 'valve grinder'
    ]
    
    # Medical and scientific equipment
    medical_equipment = [
        'stethoscope', 'blood pressure monitor', 'thermometer', 'otoscope',
        'ophthalmoscope', 'reflex hammer', 'tuning fork', 'tongue depressor',
        'syringe', 'needle', 'scalpel', 'forceps', 'surgical scissors',
        'hemostats', 'retractor', 'speculum', 'laryngoscope', 'bronchoscope',
        'endoscope', 'colonoscope', 'arthroscope', 'laparoscope', 'cystoscope',
        'ultrasound machine', 'x-ray machine', 'ct scanner', 'mri machine',
        'defibrillator', 'ecg machine', 'eeg machine', 'ventilator',
        'anesthesia machine', 'infusion pump', 'dialysis machine', 'centrifuge',
        'autoclave', 'incubator', 'microscope', 'petri dish', 'test tube',
        'beaker', 'flask', 'pipette', 'burette', 'graduated cylinder'
    ]
    
    # Sports equipment expansion
    sports_equipment = [
        'football', 'basketball', 'soccer ball', 'volleyball', 'tennis ball',
        'baseball', 'softball', 'cricket ball', 'golf ball', 'ping pong ball',
        'bowling ball', 'medicine ball', 'exercise ball', 'stability ball',
        'lacrosse ball', 'field hockey ball', 'rugby ball', 'water polo ball',
        'tennis racket', 'badminton racket', 'squash racket', 'racquetball racket',
        'ping pong paddle', 'cricket bat', 'baseball bat', 'softball bat',
        'hockey stick', 'field hockey stick', 'lacrosse stick', 'golf club',
        'driver', 'iron', 'putter', 'wedge', 'hybrid', 'fairway wood',
        'ski boots', 'ski bindings', 'ski poles', 'snowboard', 'snowboard boots',
        'ice skates', 'roller skates', 'inline skates', 'skateboard',
        'longboard', 'cruiser board', 'penny board', 'electric skateboard'
    ]
    
    # Kitchen appliances and utensils expansion
    kitchen_items = [
        'chef knife', 'paring knife', 'bread knife', 'utility knife',
        'carving knife', 'boning knife', 'fillet knife', 'cleaver',
        'santoku knife', 'nakiri knife', 'gyuto knife', 'petty knife',
        'dinner fork', 'salad fork', 'dessert fork', 'cocktail fork',
        'serving fork', 'carving fork', 'fondue fork', 'pickle fork',
        'soup spoon', 'dessert spoon', 'coffee spoon', 'serving spoon',
        'slotted spoon', 'wooden spoon', 'mixing spoon', 'measuring spoon',
        'dinner plate', 'salad plate', 'dessert plate', 'bread plate',
        'charger plate', 'soup bowl', 'cereal bowl', 'mixing bowl',
        'serving bowl', 'salad bowl', 'pasta bowl', 'rice bowl',
        'wine glass', 'beer glass', 'champagne flute', 'shot glass',
        'highball glass', 'lowball glass', 'martini glass', 'cocktail glass'
    ]
    
    # Generate all combinations
    all_objects = set()
    
    # Add base objects
    all_objects.update(base_objects)
    all_objects.update(specific_furniture)
    all_objects.update(specific_vehicles)
    all_objects.update(specific_tools)
    all_objects.update(specific_electronics)
    all_objects.update(professional_equipment)
    all_objects.update(medical_equipment)
    all_objects.update(sports_equipment)
    all_objects.update(kitchen_items)
    
    # Generate material combinations
    print("Generating material combinations...")
    for obj in base_objects[:50]:  # Limit to avoid too many combinations
        for material in materials:
            all_objects.add(f"{material} {obj}")
    
    # Generate size combinations
    print("Generating size combinations...")
    for obj in base_objects[:40]:
        for size in sizes:
            all_objects.add(f"{size} {obj}")
    
    # Generate style combinations
    print("Generating style combinations...")
    for obj in base_objects[:30]:
        for style in styles:
            all_objects.add(f"{style} {obj}")
    
    # Generate color combinations
    print("Generating color combinations...")
    for obj in base_objects[:25]:
        for color in colors:
            all_objects.add(f"{color} {obj}")
    
    # Add more specific categories
    clothing_items = [
        'shirt', 'pants', 'dress', 'skirt', 'jacket', 'coat', 'sweater',
        'hoodie', 'jeans', 'shorts', 'swimsuit', 'underwear', 'bra',
        'socks', 'stockings', 'tights', 'pajamas', 'robe', 'suit',
        'tie', 'bow tie', 'scarf', 'gloves', 'mittens', 'hat', 'cap',
        'beanie', 'helmet', 'crown', 'headband', 'glasses', 'sunglasses',
        'shoes', 'boots', 'sandals', 'slippers', 'sneakers', 'heels',
        'flip flops', 'clogs', 'loafers', 'oxfords', 'dress shoes',
        'running shoes', 'hiking boots', 'rain boots', 'snow boots'
    ]
    
    jewelry_items = [
        'ring', 'engagement ring', 'wedding ring', 'class ring', 'signet ring',
        'necklace', 'chain', 'pendant', 'choker', 'locket', 'cross',
        'earrings', 'studs', 'hoops', 'dangles', 'chandelier earrings',
        'bracelet', 'bangle', 'charm bracelet', 'tennis bracelet',
        'watch', 'digital watch', 'analog watch', 'smart watch',
        'pocket watch', 'stopwatch', 'timer', 'alarm clock',
        'brooch', 'pin', 'badge', 'cufflinks', 'tie clip', 'money clip'
    ]
    
    office_equipment = [
        'desk', 'chair', 'filing cabinet', 'bookshelf', 'computer',
        'monitor', 'keyboard', 'mouse', 'printer', 'scanner', 'copier',
        'fax machine', 'telephone', 'calculator', 'stapler', 'hole punch',
        'paper shredder', 'laminator', 'binding machine', 'label maker',
        'whiteboard', 'bulletin board', 'easel', 'projector', 'screen',
        'conference table', 'office table', 'reception desk', 'cubicle',
        'partition', 'file folder', 'binder', 'notebook', 'notepad',
        'pen', 'pencil', 'marker', 'highlighter', 'eraser', 'ruler',
        'scissors', 'tape dispenser', 'paper clips', 'rubber bands',
        'pushpins', 'thumbtacks', 'envelope', 'stamp', 'ink pad'
    ]
    
    garden_tools = [
        'shovel', 'spade', 'rake', 'hoe', 'trowel', 'pruning shears',
        'hedge trimmer', 'grass shears', 'lopper', 'chainsaw',
        'leaf blower', 'lawn mower', 'edger', 'trimmer', 'cultivator',
        'wheelbarrow', 'garden cart', 'watering can', 'hose', 'sprinkler',
        'nozzle', 'sprayer', 'fertilizer spreader', 'compost bin',
        'planter', 'flower pot', 'seed tray', 'greenhouse', 'cold frame',
        'garden stake', 'trellis', 'arbor', 'pergola', 'gazebo'
    ]
    
    bathroom_fixtures = [
        'toilet', 'sink', 'bathtub', 'shower', 'bidet', 'urinal',
        'medicine cabinet', 'mirror', 'towel rack', 'toilet paper holder',
        'soap dispenser', 'toothbrush holder', 'cup holder', 'shower curtain',
        'bath mat', 'toilet brush', 'plunger', 'scale', 'hamper',
        'wastebasket', 'tissue box', 'air freshener', 'ventilation fan'
    ]
    
    lighting_fixtures = [
        'ceiling light', 'pendant light', 'chandelier', 'track lighting',
        'recessed light', 'flush mount', 'semi flush mount', 'ceiling fan',
        'table lamp', 'floor lamp', 'desk lamp', 'reading lamp',
        'bedside lamp', 'accent lamp', 'torchiere', 'banker lamp',
        'wall sconce', 'vanity light', 'picture light', 'under cabinet light',
        'landscape lighting', 'path light', 'flood light', 'spot light',
        'string lights', 'rope lights', 'led strip', 'neon sign'
    ]
    
    # Add all these categories
    all_objects.update(clothing_items)
    all_objects.update(jewelry_items)
    all_objects.update(office_equipment)
    all_objects.update(garden_tools)
    all_objects.update(bathroom_fixtures)
    all_objects.update(lighting_fixtures)
    
    # Add automotive parts
    automotive_parts = [
        'engine', 'transmission', 'brake', 'tire', 'wheel', 'rim',
        'bumper', 'fender', 'hood', 'trunk', 'door', 'window',
        'windshield', 'mirror', 'headlight', 'taillight', 'turn signal',
        'radiator', 'battery', 'alternator', 'starter', 'spark plug',
        'air filter', 'oil filter', 'fuel filter', 'muffler', 'exhaust pipe',
        'catalytic converter', 'suspension', 'shock absorber', 'strut',
        'steering wheel', 'seat', 'seatbelt', 'airbag', 'dashboard'
    ]
    
    # Add electronic components
    electronic_components = [
        'resistor', 'capacitor', 'inductor', 'diode', 'transistor',
        'integrated circuit', 'microprocessor', 'memory chip', 'sensor',
        'switch', 'relay', 'fuse', 'circuit breaker', 'transformer',
        'motor', 'generator', 'battery', 'solar panel', 'led',
        'display', 'speaker', 'microphone', 'antenna', 'connector',
        'cable', 'wire', 'pcb', 'heat sink', 'fan', 'power supply'
    ]
    
    # Add mechanical parts
    mechanical_parts = [
        'gear', 'bearing', 'shaft', 'pulley', 'belt', 'chain',
        'sprocket', 'coupling', 'clutch', 'brake', 'spring',
        'lever', 'cam', 'piston', 'cylinder', 'valve', 'pipe',
        'fitting', 'gasket', 'seal', 'washer', 'nut', 'bolt',
        'screw', 'rivet', 'pin', 'key', 'bushing', 'sleeve'
    ]
    
    all_objects.update(automotive_parts)
    all_objects.update(electronic_components)
    all_objects.update(mechanical_parts)
    
    print(f"Generated {len(all_objects)} unique objects")
    return sorted(list(all_objects))

def main():
    objects = generate_10k_objects()
    
    # Write to file
    with open('10k_3d_objects.txt', 'w') as f:
        for obj in objects:
            f.write(obj + '\n')
    
    print(f"Saved {len(objects)} objects to 10k_3d_objects.txt")
    
    # Show first 50 as preview
    print("\nFirst 50 objects:")
    for i, obj in enumerate(objects[:50]):
        print(f"{i+1:2d}. {obj}")

if __name__ == "__main__":
    main()