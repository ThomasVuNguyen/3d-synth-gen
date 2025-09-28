#!/usr/bin/env python3
"""
Generate a list of common 3D object names using WordNet.
This script extracts concrete, physical objects that would be suitable
for 3D modeling and synthetic file generation.
"""

import nltk
from nltk.corpus import wordnet as wn
import re

def download_wordnet():
    """Download WordNet data if not already present."""
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading WordNet...")
        nltk.download('wordnet')

def is_3d_object(synset):
    """
    Check if a synset represents a physical 3D object.
    Returns True if the synset is likely a concrete, physical object.
    """
    # Get hypernyms (parent concepts)
    hypernyms = set()
    for path in synset.hypernym_paths():
        hypernyms.update([s.name() for s in path])
    
    # Physical object indicators
    physical_indicators = {
        'physical_entity.n.01',
        'object.n.01',
        'whole.n.02',
        'artifact.n.01',
        'instrumentality.n.03',
        'device.n.01',
        'container.n.01',
        'furniture.n.01',
        'vehicle.n.01',
        'structure.n.01',
        'building.n.01',
        'tool.n.01',
        'weapon.n.01',
        'clothing.n.01',
        'covering.n.01',
        'decoration.n.01',
        'equipment.n.01',
        'machine.n.01',
        'organism.n.01',
        'animal.n.01',
        'plant.n.02'
    }
    
    # Check if any hypernym indicates a physical object
    return bool(hypernyms.intersection(physical_indicators))

def get_3d_objects():
    """Extract 3D object names from WordNet."""
    objects = set()
    
    # Get all noun synsets
    for synset in wn.all_synsets('n'):
        if is_3d_object(synset):
            # Get the most common lemma (word form)
            lemma = synset.lemmas()[0].name()
            
            # Clean up the lemma
            cleaned = lemma.replace('_', ' ').lower()
            
            # Filter out unwanted patterns
            if (len(cleaned) > 2 and 
                len(cleaned) < 30 and
                not re.search(r'\d', cleaned) and
                not cleaned.startswith(('anti-', 'non-', 'pre-', 'post-')) and
                not cleaned.endswith(('ism', 'ist', 'ity', 'ness', 'tion', 'ing')) and
                ' ' not in cleaned or len(cleaned.split()) <= 3):
                objects.add(cleaned)
    
    return sorted(list(objects))

def is_proper_noun_or_place(word):
    """Check if a word is likely a proper noun, place name, or person name."""
    # Common indicators of proper nouns/places
    proper_indicators = [
        'peninsula', 'island', 'bridge', 'street', 'river', 'mountain', 'valley',
        'city', 'town', 'country', 'state', 'province', 'ocean', 'sea', 'lake',
        'bay', 'cape', 'point', 'peak', 'ridge', 'canyon', 'desert', 'forest',
        'park', 'avenue', 'road', 'lane', 'boulevard', 'plaza', 'square',
        'university', 'college', 'hospital', 'airport', 'station'
    ]
    
    # Names of places, people, or cultural groups
    place_names = {
        'america', 'american', 'europe', 'european', 'asia', 'asian', 'africa', 'african',
        'australia', 'australian', 'canada', 'canadian', 'mexico', 'mexican',
        'china', 'chinese', 'japan', 'japanese', 'korea', 'korean', 'india', 'indian',
        'brazil', 'brazilian', 'france', 'french', 'germany', 'german', 'italy', 'italian',
        'spain', 'spanish', 'russia', 'russian', 'england', 'english', 'ireland', 'irish',
        'scotland', 'scottish', 'wales', 'welsh', 'greece', 'greek', 'turkey', 'turkish',
        'zapotec', 'maya', 'aztec', 'inca', 'roman', 'viking', 'celtic', 'nordic',
        'persian', 'arabian', 'egyptian', 'phoenician', 'babylonian', 'sumerian',
        'florida', 'california', 'texas', 'alaska', 'hawaii', 'carolina', 'virginia',
        'georgia', 'pennsylvania', 'ohio', 'michigan', 'illinois', 'wisconsin',
        'london', 'paris', 'rome', 'berlin', 'madrid', 'moscow', 'tokyo', 'beijing',
        'cairo', 'athens', 'stockholm', 'copenhagen', 'oslo', 'helsinki', 'dublin',
        'amsterdam', 'brussels', 'vienna', 'budapest', 'prague', 'warsaw', 'lisbon'
    }
    
    word_lower = word.lower()
    
    # Check if it's a known place name
    if word_lower in place_names:
        return True
    
    # Check if it contains place indicators
    if any(indicator in word_lower for indicator in proper_indicators):
        return True
    
    # Check if it starts with a capital letter (after cleaning)
    if word and word[0].isupper() and len(word) > 3:
        return True
    
    return False

def is_abstract_or_non_physical(word):
    """Check if a word represents something abstract or non-physical."""
    abstract_indicators = [
        'ism', 'ist', 'ity', 'ness', 'tion', 'sion', 'ment', 'ance', 'ence',
        'ship', 'hood', 'dom', 'ward', 'wise', 'like', 'able', 'ible',
        'ology', 'ography', 'icism', 'phile', 'phobe', 'crat', 'cracy'
    ]
    
    # Chemical compounds and scientific terms
    chemical_indicators = [
        'acid', 'oxide', 'chloride', 'sulfate', 'carbonate', 'phosphate',
        'hydroxide', 'nitrate', 'bromide', 'fluoride', 'iodide', 'amine',
        'alcohol', 'ester', 'ether', 'ketone', 'aldehyde', 'polymer'
    ]
    
    # Body parts and biological terms
    biological_indicators = [
        'artery', 'vein', 'muscle', 'bone', 'cartilage', 'tissue', 'organ',
        'gland', 'nerve', 'membrane', 'ligament', 'tendon', 'joint',
        'appendage', 'appendix', 'bladder', 'kidney', 'liver', 'lung'
    ]
    
    # Abstract concepts
    abstract_concepts = [
        'potential', 'energy', 'force', 'pressure', 'resistance', 'current',
        'voltage', 'frequency', 'amplitude', 'wavelength', 'spectrum',
        'radiation', 'combustion', 'reaction', 'solution', 'mixture'
    ]
    
    word_lower = word.lower()
    
    # Check abstract suffixes
    if any(word_lower.endswith(suffix) for suffix in abstract_indicators):
        return True
    
    # Check for chemical/scientific terms
    if any(indicator in word_lower for indicator in chemical_indicators):
        return True
    
    # Check for biological terms
    if any(indicator in word_lower for indicator in biological_indicators):
        return True
    
    # Check for abstract concepts
    if any(concept in word_lower for concept in abstract_concepts):
        return True
    
    return False

def filter_common_objects(objects):
    """Filter to keep commonly known physical 3D objects."""
    # Greatly expanded curated list of common 3D objects
    curated_objects = {
        # Furniture & Home Furnishings
        'chair', 'table', 'sofa', 'bed', 'desk', 'shelf', 'cabinet', 'wardrobe',
        'stool', 'bench', 'dresser', 'nightstand', 'bookcase', 'armchair',
        'couch', 'ottoman', 'cushion', 'mattress', 'bedframe', 'headboard',
        'footstool', 'recliner', 'loveseat', 'sectional', 'futon', 'daybed',
        'bunk bed', 'crib', 'bassinet', 'highchair', 'rocking chair',
        'dining table', 'coffee table', 'end table', 'side table', 'vanity',
        'entertainment center', 'tv stand', 'credenza', 'hutch', 'buffet',
        
        # Vehicles & Transportation
        'car', 'truck', 'bus', 'motorcycle', 'bicycle', 'airplane', 'helicopter',
        'boat', 'ship', 'train', 'scooter', 'van', 'taxi', 'ambulance',
        'firetruck', 'police car', 'limousine', 'pickup truck', 'suv',
        'convertible', 'sedan', 'coupe', 'wagon', 'minivan', 'trailer',
        'yacht', 'sailboat', 'speedboat', 'canoe', 'kayak', 'submarine',
        'jet', 'glider', 'blimp', 'balloon', 'rocket', 'spaceship',
        'trolley', 'streetcar', 'subway', 'monorail', 'locomotive',
        
        # Electronics & Devices
        'computer', 'laptop', 'monitor', 'keyboard', 'mouse', 'phone', 'tablet',
        'television', 'radio', 'speaker', 'headphones', 'camera', 'printer',
        'router', 'microphone', 'gamepad', 'joystick', 'remote control',
        'smartphone', 'smartwatch', 'earbuds', 'webcam', 'projector',
        'scanner', 'modem', 'hard drive', 'usb drive', 'cd player',
        'dvd player', 'stereo', 'turntable', 'amplifier', 'mixer',
        'walkie talkie', 'intercom', 'security camera', 'alarm clock',
        
        # Kitchen & Dining
        'refrigerator', 'oven', 'microwave', 'toaster', 'blender', 'dishwasher',
        'kettle', 'pot', 'pan', 'bowl', 'plate', 'cup', 'mug', 'glass', 'bottle',
        'knife', 'fork', 'spoon', 'spatula', 'whisk', 'ladle', 'tongs',
        'cutting board', 'colander', 'strainer', 'grater', 'peeler',
        'can opener', 'bottle opener', 'corkscrew', 'rolling pin',
        'mixing bowl', 'measuring cup', 'timer', 'scale', 'juicer',
        'coffee maker', 'espresso machine', 'food processor', 'stand mixer',
        'slow cooker', 'pressure cooker', 'rice cooker', 'waffle iron',
        'griddle', 'wok', 'casserole', 'baking dish', 'roasting pan',
        
        # Tools & Hardware
        'hammer', 'screwdriver', 'wrench', 'drill', 'saw', 'ladder', 'toolbox',
        'scissors', 'pliers', 'shovel', 'rake', 'axe', 'chisel', 'file',
        'sandpaper', 'level', 'measuring tape', 'square', 'clamp',
        'hacksaw', 'jigsaw', 'circular saw', 'chainsaw', 'grinder',
        'sander', 'router', 'plane', 'awl', 'punch', 'crowbar',
        'pickaxe', 'sledgehammer', 'mallet', 'anvil', 'vise',
        
        # Home & Garden Items
        'lamp', 'clock', 'mirror', 'vase', 'pillow', 'blanket', 'towel',
        'candle', 'bucket', 'basket', 'box', 'suitcase', 'bag', 'backpack',
        'umbrella', 'fan', 'heater', 'air conditioner', 'humidifier',
        'dehumidifier', 'vacuum', 'broom', 'mop', 'duster', 'sponge',
        'brush', 'dustpan', 'trash can', 'recycling bin', 'wastebasket',
        'laundry basket', 'hamper', 'iron', 'ironing board', 'hanger',
        'clothespin', 'washing machine', 'dryer', 'clothesline',
        'garden hose', 'sprinkler', 'watering can', 'flowerpot', 'planter',
        'wheelbarrow', 'lawnmower', 'trimmer', 'pruning shears',
        
        # Sports & Recreation
        'ball', 'football', 'basketball', 'tennis ball', 'baseball bat',
        'tennis racket', 'golf club', 'skateboard', 'helmet', 'dumbbell',
        'barbell', 'weight', 'exercise bike', 'treadmill', 'rowing machine',
        'punching bag', 'hockey stick', 'hockey puck', 'soccer ball',
        'volleyball', 'ping pong paddle', 'badminton racket', 'frisbee',
        'boomerang', 'kite', 'yo-yo', 'jump rope', 'hula hoop',
        'surfboard', 'snowboard', 'skis', 'ice skates', 'roller skates',
        'scuba tank', 'snorkel', 'fins', 'goggles', 'life jacket',
        
        # Musical Instruments
        'guitar', 'piano', 'violin', 'drum', 'trumpet', 'saxophone', 'flute',
        'clarinet', 'oboe', 'bassoon', 'tuba', 'trombone', 'harmonica',
        'accordion', 'banjo', 'mandolin', 'ukulele', 'cello', 'bass',
        'harp', 'organ', 'keyboard', 'synthesizer', 'xylophone',
        'marimba', 'timpani', 'cymbals', 'tambourine', 'bongos',
        
        # Office & School Supplies
        'book', 'pen', 'pencil', 'notebook', 'binder', 'folder', 'paper',
        'stapler', 'hole punch', 'ruler', 'eraser', 'marker', 'highlighter',
        'calculator', 'protractor', 'compass', 'globe', 'map',
        'whiteboard', 'chalkboard', 'easel', 'filing cabinet', 'safe',
        'briefcase', 'portfolio', 'clipboard', 'paperclip', 'rubber band',
        
        # Clothing & Accessories
        'shoe', 'boot', 'sneaker', 'hat', 'cap', 'glasses', 'watch', 'ring',
        'necklace', 'earring', 'belt', 'tie', 'scarf', 'glove', 'mitten',
        'sock', 'sandal', 'slipper', 'purse', 'wallet', 'handbag',
        'sunglasses', 'bracelet', 'brooch', 'badge', 'pin', 'cufflink',
        
        # Building & Architecture
        'house', 'building', 'church', 'tower', 'castle', 'barn', 'garage',
        'shed', 'fence', 'gate', 'door', 'window', 'roof', 'chimney',
        'stairs', 'railing', 'balcony', 'porch', 'deck', 'patio',
        'gazebo', 'pergola', 'greenhouse', 'doghouse', 'birdhouse',
        'mailbox', 'streetlight', 'fire hydrant', 'bench', 'statue',
        
        # Food & Beverages
        'apple', 'banana', 'orange', 'pear', 'grape', 'strawberry',
        'blueberry', 'raspberry', 'blackberry', 'cherry', 'peach',
        'plum', 'apricot', 'pineapple', 'mango', 'kiwi', 'coconut',
        'watermelon', 'cantaloupe', 'honeydew', 'lemon', 'lime',
        'grapefruit', 'avocado', 'tomato', 'potato', 'carrot', 'onion',
        'garlic', 'pepper', 'cucumber', 'lettuce', 'spinach', 'broccoli',
        'cauliflower', 'cabbage', 'celery', 'corn', 'peas', 'beans',
        'bread', 'cake', 'pie', 'cookie', 'donut', 'muffin', 'bagel',
        'sandwich', 'pizza', 'hamburger', 'hot dog', 'taco', 'burrito',
        
        # Nature & Plants
        'tree', 'flower', 'plant', 'bush', 'shrub', 'cactus', 'fern',
        'grass', 'leaf', 'branch', 'twig', 'log', 'stump', 'mushroom',
        'rose', 'tulip', 'daisy', 'sunflower', 'lily', 'orchid',
        'pine tree', 'oak tree', 'maple tree', 'willow tree', 'palm tree',
        
        # Toys & Games
        'toy', 'doll', 'teddy bear', 'action figure', 'puzzle', 'board game',
        'dice', 'cards', 'chess set', 'checkers', 'dominos', 'marbles',
        'blocks', 'lego', 'robot', 'train set', 'race car', 'truck toy',
        'airplane toy', 'boat toy', 'ball toy', 'rattle', 'teething ring',
        
        # Medical & Health
        'thermometer', 'stethoscope', 'syringe', 'bandage', 'crutch',
        'wheelchair', 'walker', 'cane', 'glasses', 'contact lens',
        'hearing aid', 'pacemaker', 'prosthetic', 'brace', 'cast',
        
        # Containers & Storage
        'box', 'bag', 'container', 'jar', 'can', 'barrel', 'crate',
        'chest', 'trunk', 'bin', 'bucket', 'pail', 'tank', 'vat',
        'bottle', 'flask', 'jug', 'pitcher', 'carafe', 'decanter',
        
        # Miscellaneous Objects
        'key', 'lock', 'coin', 'trophy', 'telescope', 'microscope',
        'compass', 'magnet', 'battery', 'lightbulb', 'socket', 'plug',
        'wire', 'cable', 'rope', 'chain', 'string', 'thread',
        'needle', 'pin', 'button', 'zipper', 'velcro', 'snap'
    }
    
    # Filter WordNet objects with more lenient criteria for expansion
    filtered_objects = set()
    
    for obj in objects:
        obj_clean = obj.lower().strip()
        
        # Skip if too long or too short
        if len(obj_clean) < 3 or len(obj_clean) > 25:
            continue
            
        # Skip if contains numbers in the middle (but allow at end for sizes)
        if any(char.isdigit() for char in obj_clean[:-2]):
            continue
            
        # Skip if contains special characters
        if any(char in '()[]{}#@$%^&*+=<>?/\\|`~' for char in obj_clean):
            continue
            
        # Skip proper nouns and place names
        if is_proper_noun_or_place(obj_clean):
            continue
            
        # Skip abstract or non-physical terms
        if is_abstract_or_non_physical(obj_clean):
            continue
            
        # Skip if more than 3 words
        if len(obj_clean.split()) > 3:
            continue
        
        # More inclusive filtering - check for physical object indicators
        physical_indicators = [
            'bottle', 'cup', 'bowl', 'plate', 'glass', 'mug', 'pot', 'pan',
            'knife', 'fork', 'spoon', 'chair', 'table', 'bed', 'desk', 'lamp',
            'clock', 'book', 'pen', 'pencil', 'bag', 'box', 'ball', 'shoe',
            'hat', 'car', 'truck', 'bus', 'boat', 'plane', 'train', 'bike',
            'phone', 'camera', 'computer', 'television', 'radio', 'guitar',
            'piano', 'drum', 'violin', 'hammer', 'saw', 'drill', 'wrench',
            'tree', 'flower', 'apple', 'banana', 'orange', 'house', 'door',
            'window', 'mirror', 'vase', 'candle', 'pillow', 'towel', 'basket',
            'bucket', 'helmet', 'watch', 'ring', 'key', 'lock', 'coin',
            'toy', 'tool', 'machine', 'device', 'instrument', 'equipment',
            'furniture', 'appliance', 'container', 'vehicle', 'building'
        ]
        
        # Include objects that are likely physical
        if (obj_clean in curated_objects or
            any(indicator in obj_clean for indicator in physical_indicators) or
            obj_clean.endswith(('er', 'or', 'ing')) and len(obj_clean) > 5):
            filtered_objects.add(obj_clean)
    
    # Combine with curated list and remove duplicates
    all_objects = curated_objects.union(filtered_objects)
    
    # Final cleanup - remove obviously bad entries
    bad_patterns = [
        'ist', 'ism', 'ness', 'ment', 'tion', 'sion', 'ance', 'ence',
        'ship', 'hood', 'dom', 'ward', 'wise', 'like', 'able', 'ible',
        'ology', 'ography', 'icism', 'phile', 'phobe', 'crat', 'cracy'
    ]
    
    final_objects = set()
    for obj in all_objects:
        # Skip if ends with abstract suffixes (but allow some exceptions)
        if (any(obj.endswith(suffix) for suffix in bad_patterns) and 
            obj not in ['speaker', 'hammer', 'ladder', 'computer', 'printer']):
            continue
        
        # Keep if reasonable length and word count
        if len(obj) <= 25 and len(obj.split()) <= 3:
            final_objects.add(obj)
    
    return sorted(list(final_objects))

def main():
    print("Generating 3D object names using WordNet...")
    
    # Download WordNet if needed
    download_wordnet()
    
    # Get all 3D objects
    print("Extracting 3D objects from WordNet...")
    all_objects = get_3d_objects()
    print(f"Found {len(all_objects)} potential 3D objects")
    
    # Filter to common objects
    print("Filtering to common objects...")
    common_objects = filter_common_objects(all_objects)
    print(f"Filtered to {len(common_objects)} common 3D objects")
    
    # Save to file
    output_file = "3d_objects.txt"
    with open(output_file, 'w') as f:
        for obj in common_objects:
            f.write(obj + '\n')
    
    print(f"Saved {len(common_objects)} 3D object names to {output_file}")
    
    # Preview first 20 objects
    print("\nPreview of generated objects:")
    for i, obj in enumerate(common_objects[:20]):
        print(f"  {i+1:2d}. {obj}")
    if len(common_objects) > 20:
        print(f"  ... and {len(common_objects) - 20} more")

if __name__ == "__main__":
    main()