#!/usr/bin/env python3
"""
Generate 10,000+ 3D objects through comprehensive expansion.
"""

def generate_comprehensive_objects():
    """Generate a comprehensive list of 10,000+ 3D object names."""
    
    all_objects = set()
    
    # Base furniture with detailed variations
    furniture_base = ['chair', 'table', 'bed', 'sofa', 'desk', 'shelf', 'cabinet']
    furniture_types = {
        'chair': ['dining chair', 'office chair', 'armchair', 'rocking chair', 'folding chair', 
                  'swivel chair', 'reclining chair', 'bar chair', 'accent chair', 'lounge chair',
                  'task chair', 'ergonomic chair', 'executive chair', 'guest chair', 'stackable chair',
                  'windsor chair', 'wingback chair', 'club chair', 'barcelona chair', 'eames chair'],
        'table': ['dining table', 'coffee table', 'end table', 'side table', 'console table',
                  'kitchen table', 'picnic table', 'conference table', 'computer table', 'drafting table',
                  'folding table', 'round table', 'square table', 'rectangular table', 'oval table',
                  'glass table', 'wooden table', 'metal table', 'marble table', 'granite table'],
        'bed': ['single bed', 'double bed', 'queen bed', 'king bed', 'twin bed', 'bunk bed',
                'platform bed', 'canopy bed', 'sleigh bed', 'murphy bed', 'daybed', 'sofa bed',
                'trundle bed', 'loft bed', 'adjustable bed', 'hospital bed', 'race car bed',
                'water bed', 'air bed', 'futon bed'],
        'sofa': ['sectional sofa', 'loveseat', 'chaise lounge', 'sleeper sofa', 'reclining sofa',
                 'modular sofa', 'corner sofa', 'curved sofa', 'tufted sofa', 'chesterfield sofa',
                 'camelback sofa', 'bridgewater sofa', 'lawson sofa', 'english rolled arm sofa'],
        'desk': ['computer desk', 'writing desk', 'executive desk', 'standing desk', 'corner desk',
                 'roll top desk', 'secretary desk', 'partner desk', 'pedestal desk', 'floating desk',
                 'l shaped desk', 'u shaped desk', 'adjustable desk', 'gaming desk', 'reception desk'],
        'shelf': ['bookshelf', 'wall shelf', 'floating shelf', 'corner shelf', 'ladder shelf',
                  'cube shelf', 'industrial shelf', 'wire shelf', 'glass shelf', 'wooden shelf',
                  'metal shelf', 'display shelf', 'storage shelf', 'bathroom shelf', 'kitchen shelf'],
        'cabinet': ['kitchen cabinet', 'bathroom cabinet', 'medicine cabinet', 'filing cabinet',
                    'display cabinet', 'storage cabinet', 'base cabinet', 'wall cabinet', 'tall cabinet',
                    'corner cabinet', 'china cabinet', 'curio cabinet', 'gun cabinet', 'jewelry cabinet']
    }
    
    # Add all furniture variations
    for base, types in furniture_types.items():
        all_objects.update(types)
    
    # Materials for furniture
    materials = ['wooden', 'metal', 'plastic', 'glass', 'fabric', 'leather', 'vinyl', 'wicker',
                'rattan', 'bamboo', 'steel', 'aluminum', 'iron', 'chrome', 'brass', 'copper',
                'oak', 'pine', 'maple', 'mahogany', 'walnut', 'cherry', 'cedar', 'teak',
                'plywood', 'mdf', 'particle board', 'laminate', 'veneer', 'solid wood']
    
    # Add material combinations for furniture
    for furniture in furniture_base:
        for material in materials:
            all_objects.add(f"{material} {furniture}")
    
    # Comprehensive vehicle list
    vehicle_categories = {
        'cars': ['sedan', 'suv', 'hatchback', 'coupe', 'convertible', 'wagon', 'minivan',
                 'sports car', 'luxury car', 'economy car', 'compact car', 'midsize car',
                 'full size car', 'electric car', 'hybrid car', 'muscle car', 'vintage car',
                 'classic car', 'antique car', 'race car', 'rally car', 'drift car'],
        'trucks': ['pickup truck', 'delivery truck', 'garbage truck', 'fire truck', 'tow truck',
                   'dump truck', 'cement truck', 'logging truck', 'tanker truck', 'flatbed truck',
                   'box truck', 'refrigerated truck', 'semi truck', 'monster truck', 'food truck'],
        'buses': ['school bus', 'city bus', 'tour bus', 'charter bus', 'double decker bus',
                  'articulated bus', 'shuttle bus', 'transit bus', 'coach bus', 'party bus'],
        'motorcycles': ['sport bike', 'cruiser', 'touring bike', 'dirt bike', 'scooter',
                        'moped', 'chopper', 'cafe racer', 'dual sport', 'adventure bike'],
        'aircraft': ['airplane', 'jet', 'helicopter', 'glider', 'biplane', 'seaplane',
                     'cargo plane', 'passenger plane', 'fighter jet', 'private jet',
                     'ultralight', 'gyrocopter', 'drone', 'hot air balloon'],
        'watercraft': ['boat', 'yacht', 'sailboat', 'motorboat', 'speedboat', 'fishing boat',
                       'cruise ship', 'cargo ship', 'ferry', 'tugboat', 'submarine',
                       'catamaran', 'trimaran', 'pontoon boat', 'kayak', 'canoe']
    }
    
    for category, vehicles in vehicle_categories.items():
        all_objects.update(vehicles)
    
    # Kitchen and dining comprehensive list
    kitchen_categories = {
        'cookware': ['pot', 'pan', 'skillet', 'saucepan', 'stockpot', 'dutch oven',
                     'wok', 'frying pan', 'saute pan', 'roasting pan', 'baking dish',
                     'casserole dish', 'pressure cooker', 'slow cooker', 'steamer'],
        'utensils': ['knife', 'fork', 'spoon', 'spatula', 'whisk', 'ladle', 'tongs',
                     'can opener', 'bottle opener', 'corkscrew', 'peeler', 'grater',
                     'garlic press', 'pizza cutter', 'rolling pin', 'measuring cup'],
        'appliances': ['refrigerator', 'oven', 'microwave', 'dishwasher', 'blender',
                       'food processor', 'mixer', 'toaster', 'coffee maker', 'kettle',
                       'ice maker', 'garbage disposal', 'range hood', 'wine cooler'],
        'dinnerware': ['plate', 'bowl', 'cup', 'mug', 'glass', 'saucer', 'platter',
                       'serving bowl', 'salad bowl', 'soup bowl', 'cereal bowl', 'pasta bowl']
    }
    
    for category, items in kitchen_categories.items():
        all_objects.update(items)
    
    # Tools and hardware comprehensive expansion
    tool_categories = {
        'hand_tools': ['hammer', 'screwdriver', 'wrench', 'pliers', 'chisel', 'file',
                       'saw', 'drill', 'level', 'square', 'ruler', 'tape measure',
                       'utility knife', 'box cutter', 'awl', 'punch', 'reamer'],
        'power_tools': ['circular saw', 'jigsaw', 'reciprocating saw', 'angle grinder',
                        'belt sander', 'orbital sander', 'router', 'planer', 'jointer',
                        'drill press', 'table saw', 'miter saw', 'band saw'],
        'garden_tools': ['shovel', 'rake', 'hoe', 'trowel', 'pruning shears', 'hedge trimmer',
                         'lawn mower', 'leaf blower', 'chainsaw', 'wheelbarrow', 'watering can']
    }
    
    for category, tools in tool_categories.items():
        all_objects.update(tools)
    
    # Electronics and technology
    electronics = [
        'computer', 'laptop', 'tablet', 'smartphone', 'desktop computer', 'workstation',
        'server', 'gaming console', 'smart tv', 'monitor', 'keyboard', 'mouse',
        'printer', 'scanner', 'webcam', 'microphone', 'speaker', 'headphones',
        'router', 'modem', 'hard drive', 'ssd', 'usb drive', 'memory card',
        'camera', 'video camera', 'digital camera', 'action camera', 'security camera',
        'projector', 'smart watch', 'fitness tracker', 'e-reader', 'mp3 player'
    ]
    all_objects.update(electronics)
    
    # Sports and recreation
    sports_items = [
        'basketball', 'football', 'soccer ball', 'volleyball', 'tennis ball',
        'baseball', 'softball', 'golf ball', 'ping pong ball', 'bowling ball',
        'medicine ball', 'exercise ball', 'stability ball', 'foam roller',
        'yoga mat', 'exercise bike', 'treadmill', 'rowing machine', 'elliptical',
        'weight bench', 'dumbbell', 'barbell', 'kettlebell', 'resistance band',
        'tennis racket', 'badminton racket', 'squash racket', 'ping pong paddle',
        'baseball bat', 'cricket bat', 'hockey stick', 'golf club', 'lacrosse stick'
    ]
    all_objects.update(sports_items)
    
    # Musical instruments comprehensive
    instruments = [
        'piano', 'keyboard', 'synthesizer', 'organ', 'harpsichord', 'accordion',
        'guitar', 'acoustic guitar', 'electric guitar', 'bass guitar', 'ukulele',
        'banjo', 'mandolin', 'sitar', 'lute', 'harp', 'violin', 'viola',
        'cello', 'double bass', 'fiddle', 'trumpet', 'trombone', 'tuba',
        'french horn', 'cornet', 'bugle', 'saxophone', 'clarinet', 'oboe',
        'bassoon', 'flute', 'piccolo', 'recorder', 'harmonica', 'ocarina',
        'drums', 'drum kit', 'snare drum', 'bass drum', 'timpani', 'bongos',
        'congas', 'djembe', 'tambourine', 'cymbals', 'xylophone', 'marimba'
    ]
    all_objects.update(instruments)
    
    # Clothing and accessories detailed
    clothing = [
        'shirt', 'blouse', 'polo shirt', 't-shirt', 'tank top', 'sweater',
        'cardigan', 'hoodie', 'sweatshirt', 'jacket', 'blazer', 'coat',
        'pants', 'jeans', 'trousers', 'shorts', 'skirt', 'dress',
        'suit', 'tuxedo', 'gown', 'robe', 'pajamas', 'nightgown',
        'underwear', 'bra', 'panties', 'boxers', 'briefs', 'socks',
        'stockings', 'tights', 'pantyhose', 'shoes', 'boots', 'sneakers',
        'sandals', 'slippers', 'heels', 'flats', 'loafers', 'oxfords'
    ]
    all_objects.update(clothing)
    
    # Add jewelry and accessories
    accessories = [
        'watch', 'necklace', 'bracelet', 'ring', 'earrings', 'pendant',
        'brooch', 'cufflinks', 'tie clip', 'belt', 'wallet', 'purse',
        'handbag', 'backpack', 'briefcase', 'suitcase', 'hat', 'cap',
        'scarf', 'gloves', 'sunglasses', 'glasses', 'contact lenses'
    ]
    all_objects.update(accessories)
    
    # Home and garden items
    home_items = [
        'lamp', 'ceiling light', 'floor lamp', 'table lamp', 'desk lamp',
        'chandelier', 'pendant light', 'wall sconce', 'track lighting',
        'recessed light', 'string lights', 'mirror', 'wall mirror',
        'bathroom mirror', 'vanity mirror', 'floor mirror', 'compact mirror',
        'clock', 'wall clock', 'alarm clock', 'mantel clock', 'cuckoo clock',
        'grandfather clock', 'digital clock', 'atomic clock'
    ]
    all_objects.update(home_items)
    
    # Add household appliances
    appliances = [
        'washing machine', 'dryer', 'iron', 'vacuum cleaner', 'air conditioner',
        'heater', 'humidifier', 'dehumidifier', 'air purifier', 'fan',
        'ceiling fan', 'water heater', 'garbage disposal', 'smoke detector',
        'carbon monoxide detector', 'security system', 'thermostat'
    ]
    all_objects.update(appliances)
    
    # Office and school supplies
    office_items = [
        'pen', 'pencil', 'marker', 'highlighter', 'crayon', 'chalk',
        'eraser', 'ruler', 'protractor', 'compass', 'stapler', 'hole punch',
        'paper clips', 'rubber bands', 'pushpins', 'thumbtacks', 'binder',
        'folder', 'notebook', 'notepad', 'sticky notes', 'envelope',
        'stamp', 'calculator', 'shredder', 'laminator', 'globe', 'map'
    ]
    all_objects.update(office_items)
    
    # Food and beverages
    food_items = [
        'apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry',
        'raspberry', 'blackberry', 'cherry', 'peach', 'pear', 'plum',
        'apricot', 'mango', 'pineapple', 'coconut', 'watermelon', 'cantaloupe',
        'honeydew', 'kiwi', 'lemon', 'lime', 'grapefruit', 'avocado',
        'tomato', 'potato', 'carrot', 'onion', 'garlic', 'pepper',
        'cucumber', 'lettuce', 'spinach', 'broccoli', 'cauliflower',
        'cabbage', 'corn', 'peas', 'beans', 'celery', 'radish'
    ]
    all_objects.update(food_items)
    
    # Add prepared foods
    prepared_foods = [
        'bread', 'cake', 'pie', 'cookie', 'muffin', 'donut', 'bagel',
        'croissant', 'sandwich', 'pizza', 'hamburger', 'hot dog', 'taco',
        'burrito', 'pasta', 'spaghetti', 'soup', 'salad', 'rice', 'noodles'
    ]
    all_objects.update(prepared_foods)
    
    # Toys and games
    toys = [
        'doll', 'teddy bear', 'action figure', 'toy car', 'toy truck',
        'toy airplane', 'toy boat', 'building blocks', 'lego', 'puzzle',
        'board game', 'card game', 'video game', 'dice', 'marbles',
        'yo-yo', 'kite', 'frisbee', 'jump rope', 'hula hoop', 'slinky',
        'play dough', 'modeling clay', 'coloring book', 'crayons'
    ]
    all_objects.update(toys)
    
    # Now add combinations with materials, sizes, colors, and styles
    print("Adding material combinations...")
    
    # More comprehensive material list
    all_materials = [
        'wooden', 'metal', 'plastic', 'glass', 'ceramic', 'fabric', 'leather',
        'rubber', 'silicone', 'vinyl', 'canvas', 'denim', 'cotton', 'wool',
        'silk', 'linen', 'polyester', 'nylon', 'spandex', 'bamboo', 'cork',
        'steel', 'aluminum', 'iron', 'copper', 'brass', 'bronze', 'titanium',
        'chrome', 'stainless steel', 'cast iron', 'wrought iron', 'galvanized',
        'oak', 'pine', 'maple', 'cherry', 'walnut', 'mahogany', 'teak',
        'cedar', 'birch', 'ash', 'poplar', 'plywood', 'mdf', 'particle board',
        'marble', 'granite', 'slate', 'limestone', 'sandstone', 'concrete',
        'brick', 'stone', 'crystal', 'porcelain', 'earthenware', 'stoneware'
    ]
    
    # Size variations
    sizes = [
        'mini', 'tiny', 'small', 'compact', 'medium', 'standard', 'large',
        'extra large', 'oversized', 'giant', 'jumbo', 'pocket', 'travel',
        'portable', 'desktop', 'tabletop', 'floor', 'wall', 'ceiling',
        'commercial', 'industrial', 'professional', 'home', 'office'
    ]
    
    # Colors
    colors = [
        'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink',
        'black', 'white', 'gray', 'grey', 'brown', 'tan', 'beige',
        'cream', 'ivory', 'navy', 'royal blue', 'sky blue', 'teal',
        'turquoise', 'aqua', 'mint', 'lime', 'forest green', 'olive',
        'maroon', 'burgundy', 'crimson', 'scarlet', 'magenta', 'violet',
        'lavender', 'gold', 'silver', 'bronze', 'copper', 'rose gold'
    ]
    
    # Styles
    styles = [
        'modern', 'contemporary', 'traditional', 'classic', 'vintage',
        'antique', 'retro', 'art deco', 'mid century', 'industrial',
        'rustic', 'farmhouse', 'country', 'shabby chic', 'minimalist',
        'scandinavian', 'bohemian', 'mediterranean', 'asian', 'japanese',
        'chinese', 'french', 'italian', 'english', 'american', 'colonial',
        'victorian', 'edwardian', 'baroque', 'rococo', 'gothic', 'prairie'
    ]
    
    # Select key objects for combinations to avoid too many permutations
    key_objects = ['chair', 'table', 'lamp', 'vase', 'bowl', 'cup', 'plate',
                   'glass', 'bottle', 'pot', 'pan', 'knife', 'spoon', 'fork']
    
    # Add material combinations
    for obj in key_objects:
        for material in all_materials[:30]:  # Limit to avoid explosion
            all_objects.add(f"{material} {obj}")
    
    # Add size combinations
    for obj in key_objects:
        for size in sizes[:20]:
            all_objects.add(f"{size} {obj}")
    
    # Add color combinations
    for obj in key_objects:
        for color in colors[:25]:
            all_objects.add(f"{color} {obj}")
    
    # Add style combinations
    for obj in key_objects:
        for style in styles[:20]:
            all_objects.add(f"{style} {obj}")
    
    # Add specific technical objects
    technical_objects = [
        'oscilloscope', 'multimeter', 'function generator', 'power supply',
        'spectrum analyzer', 'signal generator', 'logic analyzer', 'voltmeter',
        'ammeter', 'ohmmeter', 'frequency counter', 'capacitance meter',
        'lcr meter', 'insulation tester', 'earth tester', 'clamp meter',
        'phase meter', 'waveform generator', 'arbitrary waveform generator',
        'rf generator', 'microwave generator', 'sweep generator', 'pulse generator'
    ]
    all_objects.update(technical_objects)
    
    # Add more categories to reach 10k
    
    # Automotive parts
    auto_parts = [
        'engine', 'transmission', 'brake pad', 'brake disc', 'tire', 'wheel',
        'rim', 'hubcap', 'bumper', 'fender', 'hood', 'trunk', 'door handle',
        'window', 'windshield', 'side mirror', 'rearview mirror', 'headlight',
        'taillight', 'turn signal', 'license plate', 'exhaust pipe', 'muffler',
        'catalytic converter', 'radiator', 'battery', 'alternator', 'starter',
        'distributor', 'spark plug', 'ignition coil', 'fuel pump', 'carburetor',
        'throttle body', 'intake manifold', 'exhaust manifold', 'cylinder head',
        'piston', 'connecting rod', 'crankshaft', 'camshaft', 'timing belt'
    ]
    all_objects.update(auto_parts)
    
    # Electronic components
    electronic_parts = [
        'resistor', 'capacitor', 'inductor', 'diode', 'transistor', 'mosfet',
        'integrated circuit', 'microcontroller', 'microprocessor', 'memory chip',
        'flash memory', 'eeprom', 'ram', 'rom', 'cpu', 'gpu', 'fpga',
        'dsp', 'adc', 'dac', 'op amp', 'voltage regulator', 'crystal oscillator',
        'relay', 'switch', 'potentiometer', 'encoder', 'decoder', 'multiplexer',
        'demultiplexer', 'logic gate', 'flip flop', 'counter', 'timer',
        'sensor', 'accelerometer', 'gyroscope', 'magnetometer', 'pressure sensor',
        'temperature sensor', 'humidity sensor', 'light sensor', 'proximity sensor'
    ]
    all_objects.update(electronic_parts)
    
    # Mechanical parts
    mechanical_parts = [
        'gear', 'spur gear', 'helical gear', 'bevel gear', 'worm gear',
        'planetary gear', 'bearing', 'ball bearing', 'roller bearing',
        'thrust bearing', 'sleeve bearing', 'shaft', 'axle', 'spindle',
        'coupling', 'universal joint', 'cv joint', 'clutch', 'brake',
        'spring', 'coil spring', 'leaf spring', 'torsion spring', 'gas spring',
        'damper', 'shock absorber', 'strut', 'lever', 'linkage', 'cam',
        'follower', 'piston', 'cylinder', 'rod', 'pin', 'key', 'keyway',
        'spline', 'thread', 'screw thread', 'bolt', 'nut', 'washer',
        'gasket', 'seal', 'o-ring', 'bushing', 'sleeve', 'collar'
    ]
    all_objects.update(mechanical_parts)
    
    # Building materials and hardware
    building_materials = [
        'brick', 'concrete block', 'lumber', 'plywood', 'drywall', 'insulation',
        'roofing shingle', 'siding', 'window frame', 'door frame', 'molding',
        'trim', 'baseboard', 'crown molding', 'chair rail', 'wainscoting',
        'flooring', 'hardwood flooring', 'laminate flooring', 'vinyl flooring',
        'carpet', 'tile', 'ceramic tile', 'porcelain tile', 'stone tile',
        'marble tile', 'granite tile', 'slate tile', 'glass tile', 'mosaic tile'
    ]
    all_objects.update(building_materials)
    
    # Hardware and fasteners
    hardware = [
        'screw', 'wood screw', 'machine screw', 'sheet metal screw', 'drywall screw',
        'concrete screw', 'self tapping screw', 'bolt', 'hex bolt', 'carriage bolt',
        'lag bolt', 'anchor bolt', 'eye bolt', 'u bolt', 'j bolt', 'toggle bolt',
        'nail', 'finish nail', 'brad nail', 'roofing nail', 'concrete nail',
        'masonry nail', 'spiral nail', 'ring shank nail', 'staple', 'rivet',
        'pop rivet', 'blind rivet', 'solid rivet', 'pin', 'cotter pin',
        'spring pin', 'dowel pin', 'taper pin', 'clevis pin', 'hinge pin'
    ]
    all_objects.update(hardware)
    
    print(f"Generated {len(all_objects)} unique objects")
    return sorted(list(all_objects))

def main():
    objects = generate_comprehensive_objects()
    
    # Write to file
    with open('10k_3d_objects.txt', 'w') as f:
        for obj in objects:
            f.write(obj + '\n')
    
    print(f"Saved {len(objects)} objects to 10k_3d_objects.txt")
    
    # Show statistics
    print(f"\nGenerated {len(objects)} total objects")
    if len(objects) >= 10000:
        print("✅ Successfully reached 10,000+ objects!")
    else:
        print(f"📊 {10000 - len(objects)} more objects needed to reach 10,000")
    
    # Show first 50 as preview
    print("\nFirst 50 objects:")
    for i, obj in enumerate(objects[:50]):
        print(f"{i+1:2d}. {obj}")

if __name__ == "__main__":
    main()