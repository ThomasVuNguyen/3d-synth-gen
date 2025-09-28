#!/usr/bin/env python3
"""
Generate 10,000+ 3D objects through massive systematic expansion.
"""

def generate_massive_object_list():
    """Generate a massive list of 10,000+ 3D object names."""
    
    all_objects = set()
    
    # Start with comprehensive base categories
    
    # FURNITURE - Massively expanded
    furniture_base = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'bench',
        'stool', 'dresser', 'nightstand', 'wardrobe', 'bookcase', 'credenza',
        'ottoman', 'armchair', 'recliner', 'loveseat', 'sectional', 'futon'
    ]
    
    furniture_specific = [
        'accent chair', 'bar stool', 'counter stool', 'piano bench', 'park bench',
        'dining chair', 'office chair', 'rocking chair', 'folding chair', 'swivel chair',
        'ergonomic chair', 'executive chair', 'guest chair', 'task chair', 'club chair',
        'wingback chair', 'barcelona chair', 'eames chair', 'windsor chair', 'parsons chair',
        'coffee table', 'dining table', 'end table', 'side table', 'console table',
        'conference table', 'kitchen table', 'picnic table', 'pool table', 'drafting table',
        'computer table', 'sofa table', 'accent table', 'nesting table', 'trestle table',
        'single bed', 'twin bed', 'full bed', 'queen bed', 'king bed', 'california king bed',
        'daybed', 'bunk bed', 'loft bed', 'murphy bed', 'platform bed', 'canopy bed',
        'sleigh bed', 'poster bed', 'panel bed', 'storage bed', 'adjustable bed',
        'sectional sofa', 'sleeper sofa', 'reclining sofa', 'chaise lounge', 'modular sofa',
        'computer desk', 'writing desk', 'executive desk', 'standing desk', 'corner desk',
        'roll top desk', 'secretary desk', 'pedestal desk', 'l shaped desk', 'u shaped desk'
    ]
    
    all_objects.update(furniture_base)
    all_objects.update(furniture_specific)
    
    # VEHICLES - Massively expanded
    vehicles = [
        # Cars by type
        'sedan', 'hatchback', 'coupe', 'convertible', 'wagon', 'suv', 'crossover',
        'minivan', 'pickup truck', 'sports car', 'luxury car', 'economy car', 'compact car',
        'midsize car', 'full size car', 'subcompact car', 'muscle car', 'supercar',
        'hypercar', 'electric car', 'hybrid car', 'diesel car', 'police car', 'taxi',
        'ambulance', 'fire truck', 'limousine', 'hearse', 'race car', 'rally car',
        'drag car', 'drift car', 'stock car', 'formula car', 'go kart', 'atv', 'utv',
        
        # Trucks
        'delivery truck', 'box truck', 'panel truck', 'flatbed truck', 'dump truck',
        'garbage truck', 'tow truck', 'cement truck', 'tanker truck', 'logging truck',
        'crane truck', 'fire truck', 'food truck', 'ice cream truck', 'mail truck',
        'moving truck', 'pickup truck', 'semi truck', 'monster truck', 'snow plow',
        
        # Buses
        'school bus', 'city bus', 'tour bus', 'charter bus', 'shuttle bus', 'coach bus',
        'double decker bus', 'articulated bus', 'trolley bus', 'minibus', 'party bus',
        
        # Motorcycles
        'sport bike', 'cruiser', 'touring bike', 'dirt bike', 'dual sport', 'adventure bike',
        'cafe racer', 'bobber', 'chopper', 'naked bike', 'supermoto', 'enduro',
        'trial bike', 'moped', 'scooter', 'vespa', 'electric bike', 'three wheeler',
        
        # Aircraft
        'airplane', 'jet', 'helicopter', 'glider', 'biplane', 'seaplane', 'floatplane',
        'cargo plane', 'passenger plane', 'fighter jet', 'bomber', 'private jet',
        'business jet', 'ultralight', 'gyrocopter', 'autogyro', 'drone', 'quadcopter',
        'hot air balloon', 'airship', 'blimp', 'dirigible', 'rocket', 'spacecraft',
        
        # Watercraft
        'boat', 'yacht', 'sailboat', 'motorboat', 'speedboat', 'pontoon boat', 'fishing boat',
        'cabin cruiser', 'center console', 'bowrider', 'ski boat', 'wake boat', 'jet ski',
        'canoe', 'kayak', 'raft', 'dinghy', 'rowboat', 'pedal boat', 'catamaran',
        'trimaran', 'houseboat', 'tugboat', 'barge', 'ferry', 'cruise ship', 'cargo ship',
        'container ship', 'oil tanker', 'submarine', 'destroyer', 'aircraft carrier'
    ]
    all_objects.update(vehicles)
    
    # TOOLS - Comprehensive expansion
    hand_tools = [
        'hammer', 'claw hammer', 'ball peen hammer', 'sledge hammer', 'framing hammer',
        'tack hammer', 'dead blow hammer', 'rubber mallet', 'wooden mallet', 'rawhide mallet',
        'screwdriver', 'flat head screwdriver', 'phillips screwdriver', 'torx screwdriver',
        'hex screwdriver', 'precision screwdriver', 'stubby screwdriver', 'offset screwdriver',
        'wrench', 'combination wrench', 'box wrench', 'open end wrench', 'socket wrench',
        'pipe wrench', 'monkey wrench', 'torque wrench', 'allen wrench', 'hex wrench',
        'basin wrench', 'strap wrench', 'chain wrench', 'adjustable wrench', 'ratcheting wrench',
        'pliers', 'needle nose pliers', 'slip joint pliers', 'locking pliers', 'wire cutters',
        'diagonal cutters', 'lineman pliers', 'fence pliers', 'crimping pliers', 'welding pliers',
        'saw', 'hand saw', 'crosscut saw', 'rip saw', 'back saw', 'dovetail saw', 'coping saw',
        'fret saw', 'keyhole saw', 'hacksaw', 'bow saw', 'pruning saw', 'folding saw'
    ]
    
    power_tools = [
        'drill', 'cordless drill', 'hammer drill', 'impact drill', 'right angle drill',
        'drill press', 'bench drill', 'magnetic drill', 'masonry drill', 'core drill',
        'circular saw', 'table saw', 'miter saw', 'compound miter saw', 'radial arm saw',
        'band saw', 'scroll saw', 'jigsaw', 'reciprocating saw', 'track saw', 'panel saw',
        'grinder', 'angle grinder', 'bench grinder', 'die grinder', 'straight grinder',
        'sander', 'belt sander', 'orbital sander', 'palm sander', 'disc sander', 'drum sander',
        'router', 'plunge router', 'fixed base router', 'trim router', 'laminate trimmer',
        'planer', 'thickness planer', 'hand planer', 'jointer', 'biscuit joiner',
        'nailer', 'brad nailer', 'finish nailer', 'framing nailer', 'roofing nailer',
        'stapler', 'pneumatic stapler', 'electric stapler', 'manual stapler'
    ]
    
    all_objects.update(hand_tools)
    all_objects.update(power_tools)
    
    # ELECTRONICS - Massive expansion
    computers = [
        'desktop computer', 'laptop computer', 'notebook computer', 'netbook', 'ultrabook',
        'tablet computer', 'ipad', 'surface tablet', 'chromebook', 'macbook', 'imac',
        'pc', 'workstation', 'server', 'mini computer', 'single board computer',
        'gaming computer', 'all in one computer', 'tower computer', 'mini tower',
        'micro tower', 'small form factor', 'rack server', 'blade server'
    ]
    
    phones = [
        'smartphone', 'cell phone', 'mobile phone', 'iphone', 'android phone', 'flip phone',
        'slider phone', 'cordless phone', 'landline phone', 'desk phone', 'wall phone',
        'rotary phone', 'push button phone', 'satellite phone', 'two way radio',
        'walkie talkie', 'ham radio', 'cb radio', 'shortwave radio', 'weather radio'
    ]
    
    cameras = [
        'digital camera', 'film camera', 'instant camera', 'polaroid camera', 'disposable camera',
        'slr camera', 'dslr camera', 'mirrorless camera', 'point and shoot camera',
        'action camera', 'gopro', 'security camera', 'surveillance camera', 'webcam',
        'video camera', 'camcorder', 'film camera', '35mm camera', 'medium format camera',
        'large format camera', 'pinhole camera', 'panoramic camera', 'stereo camera'
    ]
    
    audio_equipment = [
        'speaker', 'bookshelf speaker', 'floor speaker', 'subwoofer', 'tweeter', 'woofer',
        'bluetooth speaker', 'wireless speaker', 'portable speaker', 'computer speaker',
        'headphones', 'earphones', 'earbuds', 'wireless headphones', 'noise canceling headphones',
        'studio headphones', 'gaming headset', 'microphone', 'dynamic microphone',
        'condenser microphone', 'ribbon microphone', 'lavalier microphone', 'shotgun microphone',
        'radio', 'am radio', 'fm radio', 'clock radio', 'portable radio', 'boombox',
        'stereo system', 'hi fi system', 'turntable', 'record player', 'cd player',
        'cassette player', 'mp3 player', 'ipod', 'walkman', 'amplifier', 'receiver',
        'equalizer', 'mixer', 'audio interface', 'dac', 'preamp'
    ]
    
    all_objects.update(computers)
    all_objects.update(phones)
    all_objects.update(cameras)
    all_objects.update(audio_equipment)
    
    # Add comprehensive materials
    materials = [
        'wooden', 'oak', 'pine', 'maple', 'cherry', 'walnut', 'mahogany', 'teak', 'cedar',
        'birch', 'ash', 'poplar', 'bamboo', 'cork', 'plywood', 'mdf', 'particle board',
        'hardwood', 'softwood', 'reclaimed wood', 'engineered wood', 'laminate', 'veneer',
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
    
    # Add comprehensive colors
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
    
    # Add comprehensive sizes
    sizes = [
        'mini', 'micro', 'tiny', 'small', 'compact', 'petite', 'medium', 'standard',
        'regular', 'large', 'big', 'extra large', 'xl', 'xxl', 'oversized', 'giant',
        'jumbo', 'massive', 'huge', 'enormous', 'pocket', 'travel', 'portable',
        'desktop', 'tabletop', 'countertop', 'floor', 'standing', 'wall', 'ceiling',
        'commercial', 'industrial', 'professional', 'residential', 'home', 'office',
        'studio', 'deluxe', 'premium', 'luxury', 'economy', 'basic', 'entry level'
    ]
    
    # Add comprehensive styles
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
    
    # Generate combinations for key objects
    key_objects = [
        'chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet', 'lamp', 'mirror',
        'vase', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle', 'pot', 'pan',
        'knife', 'fork', 'spoon', 'clock', 'picture', 'frame', 'box', 'basket',
        'bin', 'container', 'jar', 'can', 'bag', 'purse', 'wallet', 'case'
    ]
    
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
    
    # Add massive kitchen and dining items
    kitchen_items = [
        'pot', 'saucepan', 'stockpot', 'dutch oven', 'pressure cooker', 'slow cooker',
        'rice cooker', 'steamer', 'double boiler', 'roasting pan', 'baking dish',
        'casserole dish', 'skillet', 'frying pan', 'saute pan', 'grill pan', 'wok',
        'crepe pan', 'omelet pan', 'paella pan', 'tagine', 'griddle', 'grill',
        'knife', 'chef knife', 'paring knife', 'bread knife', 'carving knife',
        'utility knife', 'boning knife', 'fillet knife', 'cleaver', 'steak knife',
        'butter knife', 'cheese knife', 'oyster knife', 'pizza cutter', 'mandoline',
        'fork', 'dinner fork', 'salad fork', 'dessert fork', 'cocktail fork',
        'serving fork', 'carving fork', 'pasta fork', 'fondue fork',
        'spoon', 'tablespoon', 'teaspoon', 'soup spoon', 'dessert spoon',
        'serving spoon', 'slotted spoon', 'wooden spoon', 'ladle', 'skimmer',
        'spatula', 'turner', 'fish spatula', 'offset spatula', 'rubber spatula',
        'whisk', 'balloon whisk', 'flat whisk', 'spiral whisk', 'danish whisk',
        'tongs', 'salad tongs', 'ice tongs', 'pasta tongs', 'grill tongs',
        'peeler', 'vegetable peeler', 'julienne peeler', 'zester', 'grater',
        'box grater', 'microplane', 'nutmeg grater', 'cheese grater', 'garlic press',
        'can opener', 'bottle opener', 'corkscrew', 'wine opener', 'jar opener',
        'measuring cup', 'liquid measuring cup', 'dry measuring cup', 'measuring spoon',
        'kitchen scale', 'food scale', 'timer', 'thermometer', 'meat thermometer',
        'candy thermometer', 'oven thermometer', 'refrigerator thermometer'
    ]
    all_objects.update(kitchen_items)
    
    # Add comprehensive appliances
    appliances = [
        'refrigerator', 'french door refrigerator', 'side by side refrigerator',
        'top freezer refrigerator', 'bottom freezer refrigerator', 'mini fridge',
        'wine refrigerator', 'beverage cooler', 'ice maker', 'water dispenser',
        'oven', 'gas oven', 'electric oven', 'convection oven', 'toaster oven',
        'countertop oven', 'steam oven', 'combination oven', 'pizza oven', 'microwave',
        'countertop microwave', 'over the range microwave', 'built in microwave',
        'dishwasher', 'built in dishwasher', 'portable dishwasher', 'countertop dishwasher',
        'range', 'gas range', 'electric range', 'induction range', 'dual fuel range',
        'cooktop', 'gas cooktop', 'electric cooktop', 'induction cooktop', 'range hood',
        'washing machine', 'front load washer', 'top load washer', 'compact washer',
        'dryer', 'electric dryer', 'gas dryer', 'heat pump dryer', 'washer dryer combo',
        'air conditioner', 'central air', 'window ac', 'portable ac', 'mini split',
        'heat pump', 'furnace', 'boiler', 'water heater', 'tankless water heater',
        'vacuum cleaner', 'upright vacuum', 'canister vacuum', 'handheld vacuum',
        'robot vacuum', 'stick vacuum', 'shop vacuum', 'steam cleaner', 'carpet cleaner'
    ]
    all_objects.update(appliances)
    
    # Add comprehensive household items
    household_items = [
        'basket', 'laundry basket', 'storage basket', 'picnic basket', 'fruit basket',
        'bread basket', 'wastepaper basket', 'hamper', 'clothes hamper', 'toy box',
        'storage box', 'jewelry box', 'tool box', 'lunch box', 'music box',
        'bin', 'storage bin', 'recycling bin', 'compost bin', 'trash bin',
        'bucket', 'mop bucket', 'ice bucket', 'paint bucket', 'cleaning bucket',
        'mop', 'string mop', 'sponge mop', 'microfiber mop', 'steam mop',
        'broom', 'push broom', 'corn broom', 'whisk broom', 'dustpan',
        'vacuum', 'carpet sweeper', 'floor sweeper', 'duster', 'feather duster',
        'microfiber duster', 'cleaning cloth', 'cleaning rag', 'paper towel',
        'toilet paper', 'tissue', 'napkin', 'place mat', 'table runner',
        'tablecloth', 'shower curtain', 'window curtain', 'drapes', 'blinds',
        'shade', 'valance', 'cornice', 'rod', 'curtain rod', 'drapery rod'
    ]
    all_objects.update(household_items)
    
    # Add comprehensive office supplies
    office_supplies = [
        'pen', 'ballpoint pen', 'gel pen', 'felt tip pen', 'marker pen', 'fountain pen',
        'rollerball pen', 'pencil', 'mechanical pencil', 'colored pencil', 'drawing pencil',
        'marker', 'permanent marker', 'dry erase marker', 'highlighter', 'crayon',
        'chalk', 'charcoal', 'eraser', 'gum eraser', 'kneaded eraser', 'pink eraser',
        'ruler', 'metal ruler', 'plastic ruler', 'wooden ruler', 'yardstick',
        'measuring tape', 'protractor', 'compass', 'triangle', 'square', 't square',
        'stapler', 'desktop stapler', 'handheld stapler', 'electric stapler',
        'heavy duty stapler', 'staple remover', 'staples', 'paper clips',
        'binder clips', 'bull clips', 'pushpins', 'thumbtacks', 'rubber bands',
        'tape', 'scotch tape', 'masking tape', 'duct tape', 'packing tape',
        'tape dispenser', 'label maker', 'labels', 'hole punch', 'three hole punch',
        'single hole punch', 'paper shredder', 'laminator', 'laminating pouches',
        'calculator', 'desktop calculator', 'scientific calculator', 'graphing calculator',
        'adding machine', 'cash register', 'time clock', 'punch clock'
    ]
    all_objects.update(office_supplies)
    
    # Add automotive parts
    auto_parts = [
        'engine', 'v6 engine', 'v8 engine', 'diesel engine', 'hybrid engine',
        'transmission', 'manual transmission', 'automatic transmission', 'cvt',
        'brake', 'brake pad', 'brake rotor', 'brake caliper', 'brake drum',
        'tire', 'all season tire', 'winter tire', 'summer tire', 'performance tire',
        'wheel', 'alloy wheel', 'steel wheel', 'chrome wheel', 'rim', 'hubcap',
        'bumper', 'front bumper', 'rear bumper', 'fender', 'quarter panel',
        'hood', 'trunk', 'tailgate', 'door', 'car door', 'door handle',
        'window', 'windshield', 'rear window', 'side window', 'sunroof', 'moonroof',
        'mirror', 'side mirror', 'rearview mirror', 'blind spot mirror',
        'headlight', 'halogen headlight', 'led headlight', 'hid headlight',
        'taillight', 'brake light', 'turn signal', 'hazard light', 'fog light',
        'license plate', 'license plate frame', 'exhaust pipe', 'muffler',
        'catalytic converter', 'tail pipe', 'resonator', 'header', 'manifold',
        'radiator', 'cooling fan', 'water pump', 'thermostat', 'hose',
        'battery', 'car battery', 'alternator', 'starter', 'distributor',
        'spark plug', 'ignition coil', 'fuel pump', 'fuel filter', 'air filter',
        'oil filter', 'cabin filter', 'carburetor', 'fuel injector', 'throttle body'
    ]
    all_objects.update(auto_parts)
    
    print(f"Generated {len(all_objects)} unique objects so far...")
    
    # Add even more combinations to reach 10k
    print("Adding final combinations to reach 10k...")
    
    # Generate room-specific furniture
    rooms = ['living room', 'bedroom', 'dining room', 'kitchen', 'bathroom', 'office',
             'family room', 'den', 'study', 'nursery', 'guest room', 'master bedroom']
    
    for room in rooms:
        for obj in key_objects[:10]:
            all_objects.add(f"{room} {obj}")
    
    # Add condition modifiers
    conditions = ['new', 'used', 'vintage', 'antique', 'refurbished', 'restored',
                  'damaged', 'broken', 'cracked', 'chipped', 'scratched', 'dented']
    
    for condition in conditions:
        for obj in key_objects[:15]:
            all_objects.add(f"{condition} {obj}")
    
    # Add brand-style modifiers
    brands = ['designer', 'luxury', 'premium', 'high end', 'custom', 'handmade',
              'artisan', 'imported', 'italian', 'german', 'japanese', 'american']
    
    for brand in brands:
        for obj in key_objects[:15]:
            all_objects.add(f"{brand} {obj}")
    
    # Add functional modifiers
    functions = ['adjustable', 'foldable', 'stackable', 'portable', 'electric',
                 'manual', 'automatic', 'digital', 'analog', 'wireless', 'bluetooth']
    
    for function in functions:
        for obj in key_objects[:15]:
            all_objects.add(f"{function} {obj}")
    
    print(f"Final count: {len(all_objects)} unique objects")
    return sorted(list(all_objects))

def main():
    objects = generate_massive_object_list()
    
    # Write to file
    with open('10k_3d_objects.txt', 'w') as f:
        for obj in objects:
            f.write(obj + '\n')
    
    print(f"\\nSaved {len(objects)} objects to 10k_3d_objects.txt")
    
    if len(objects) >= 10000:
        print("✅ Successfully reached 10,000+ objects!")
    else:
        print(f"📊 {10000 - len(objects)} more objects needed to reach 10,000")
    
    # Show first 100 as preview
    print("\\nFirst 100 objects:")
    for i, obj in enumerate(objects[:100]):
        print(f"{i+1:3d}. {obj}")

if __name__ == "__main__":
    main()