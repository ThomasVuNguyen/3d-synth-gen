#!/usr/bin/env python3

import os
import gc
import cv2
import torch
import numpy as np
from datasets import load_dataset, Dataset, Features, Value, Image as HFImage
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io
from typing import Tuple, List, Dict, Any

class RobustImageFilter:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        """Initialize the robust image filter with CLIP model"""
        print(f"Loading CLIP model: {model_name}")
        self.model = CLIPModel.from_pretrained(model_name)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.device = torch.device("cpu")  # Force CPU due to CUDA compatibility issues
        self.model.to(self.device)
        print(f"Model loaded on device: {self.device}")

    def basic_quality_check(self, image: Image.Image) -> Tuple[bool, str]:
        """Check basic image quality to filter out empty/dark/low-detail images"""
        try:
            # Convert PIL to numpy array
            img_array = np.array(image)

            # Handle different image modes
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                # RGB image
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            elif len(img_array.shape) == 2:
                # Already grayscale
                gray = img_array
            else:
                return False, "invalid_format"

            # Check if image is mostly empty/black
            mean_brightness = np.mean(gray)
            if mean_brightness < 10:
                return False, "too_dark"

            # Check if image is mostly white/overexposed
            if mean_brightness > 245:
                return False, "overexposed"

            # Check if image has enough detail/edges
            edges = cv2.Canny(gray, 50, 150)
            edge_ratio = np.sum(edges > 0) / edges.size

            if edge_ratio < 0.001:  # Less than 0.1% edges
                return False, "no_detail"

            # Check for sufficient contrast
            contrast = np.std(gray)
            if contrast < 10:
                return False, "low_contrast"

            return True, "quality_ok"

        except Exception as e:
            return False, f"quality_check_error: {str(e)}"

    def check_object_presence(self, image: Image.Image) -> Tuple[bool, str, float]:
        """Check if image contains any recognizable 3D object"""
        try:
            general_candidates = [
                "a recognizable 3D object",
                "geometric shapes and primitives only",
                "an empty 3D scene",
                "abstract unrecognizable geometry"
            ]

            inputs = self.processor(
                text=general_candidates,
                images=image,
                return_tensors="pt",
                padding=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = outputs.logits_per_image.softmax(dim=1)

            object_prob = float(probs[0][0])  # "recognizable 3D object" probability

            if object_prob > 0.6:
                return True, "has_object", object_prob
            elif object_prob > 0.4:
                return False, "unclear_object", object_prob
            else:
                return False, "no_object", object_prob

        except Exception as e:
            return False, f"object_presence_error: {str(e)}", 0.0

    def check_object_match(self, image: Image.Image, object_name: str) -> Tuple[bool, str, float]:
        """Check if the detected object matches the expected object name"""
        try:
            # Create variations of the target object description
            object_variations = [
                f"a {object_name}",
                f"a 3D model of a {object_name}",
                f"a rendered {object_name}",
                f"{object_name}"
            ]

            # Create negative examples
            negative_examples = [
                "a different unrelated object",
                "the wrong type of object",
                "an object that doesn't match the description",
                "something else entirely"
            ]

            all_candidates = object_variations + negative_examples

            inputs = self.processor(
                text=all_candidates,
                images=image,
                return_tensors="pt",
                padding=True
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = outputs.logits_per_image.softmax(dim=1)

            # Sum probabilities for target object variations
            target_prob = float(probs[0][:len(object_variations)].sum())
            negative_prob = float(probs[0][len(object_variations):].sum())

            if target_prob > 0.65:
                return True, "strong_match", target_prob
            elif target_prob > 0.45:
                return True, "weak_match", target_prob
            elif target_prob > negative_prob:
                return False, "possible_wrong_object", target_prob
            else:
                return False, "wrong_object", target_prob

        except Exception as e:
            return False, f"object_match_error: {str(e)}", 0.0

    def comprehensive_filter(self, image: Image.Image, object_name: str) -> Dict[str, Any]:
        """Run comprehensive filtering pipeline on a single image"""
        result = {
            'passed': False,
            'reason': '',
            'quality_check': {},
            'object_presence': {},
            'object_match': {},
            'final_confidence': 0.0
        }

        # Stage 1: Basic quality check
        quality_ok, quality_reason = self.basic_quality_check(image)
        result['quality_check'] = {
            'passed': quality_ok,
            'reason': quality_reason
        }

        if not quality_ok:
            result['reason'] = f"quality_failed: {quality_reason}"
            return result

        # Stage 2: Check for object presence
        has_object, presence_reason, presence_confidence = self.check_object_presence(image)
        result['object_presence'] = {
            'has_object': has_object,
            'reason': presence_reason,
            'confidence': presence_confidence
        }

        if not has_object:
            result['reason'] = f"no_object: {presence_reason}"
            return result

        # Stage 3: Check object match
        matches, match_reason, match_confidence = self.check_object_match(image, object_name)
        result['object_match'] = {
            'matches': matches,
            'reason': match_reason,
            'confidence': match_confidence
        }

        # Calculate final confidence score
        final_confidence = (presence_confidence * 0.3 + match_confidence * 0.7)
        result['final_confidence'] = final_confidence

        if matches and match_reason in ['strong_match', 'weak_match']:
            result['passed'] = True
            result['reason'] = f"passed: {match_reason}"
        else:
            result['reason'] = f"object_mismatch: {match_reason}"

        return result

def process_parquet_file(parquet_path: str, filter_obj: RobustImageFilter, output_dir: str) -> Dict[str, int]:
    """Process a single parquet file and create filtered version"""
    print(f"Processing {parquet_path}")

    # Load the dataset
    ds = load_dataset('parquet', data_files=parquet_path, split='train')

    filtered_data = []
    stats = {
        'total': len(ds),
        'passed': 0,
        'failed_quality': 0,
        'failed_no_object': 0,
        'failed_wrong_object': 0,
        'failed_error': 0
    }

    for i, item in enumerate(ds):
        # Skip items that already have errors
        if item['error'] is not None and item['error'] != '':
            stats['failed_error'] += 1
            continue

        # Skip items without images
        if item['image'] is None:
            stats['failed_error'] += 1
            continue

        # Extract object name from input
        object_name = item['input'].strip()

        # Run comprehensive filtering
        filter_result = filter_obj.comprehensive_filter(item['image'], object_name)

        # Update statistics
        if filter_result['passed']:
            stats['passed'] += 1
            # Keep the item
            filtered_data.append({
                'input': item['input'],
                'script': item['script'],
                'image': item['image'],
                'error': item['error'],
                'filter_confidence': filter_result['final_confidence'],
                'filter_reason': filter_result['reason']
            })
        else:
            # Categorize failure reason
            if 'quality_failed' in filter_result['reason']:
                stats['failed_quality'] += 1
            elif 'no_object' in filter_result['reason']:
                stats['failed_no_object'] += 1
            elif 'object_mismatch' in filter_result['reason']:
                stats['failed_wrong_object'] += 1
            else:
                stats['failed_error'] += 1

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(ds)} items, {stats['passed']} passed so far")

    # Save filtered data if any items passed
    if filtered_data:
        # Define features for the filtered dataset
        features = Features({
            'input': Value('string'),
            'script': Value('string'),
            'image': HFImage(),
            'error': Value('string'),
            'filter_confidence': Value('float64'),
            'filter_reason': Value('string')
        })

        filtered_ds = Dataset.from_list(filtered_data, features=features)

        # Create output filename
        input_filename = os.path.basename(parquet_path)
        output_filename = input_filename.replace('.parquet', '_filtered.parquet')
        output_path = os.path.join(output_dir, output_filename)

        filtered_ds.to_parquet(output_path)
        print(f"  Saved {len(filtered_data)} filtered items to {output_filename}")

    # Clean up memory
    del ds
    del filtered_data
    gc.collect()

    return stats

def main():
    """Main function to process all parquet files"""
    input_dir = "3dgen_filtered_parquets"
    output_dir = "3dgen_robust_filtered"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize the filter
    filter_obj = RobustImageFilter()

    # Get all parquet files
    parquet_files = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith('.parquet')
    ])

    print(f"Found {len(parquet_files)} parquet files to process")

    # Process each file
    total_stats = {
        'total': 0,
        'passed': 0,
        'failed_quality': 0,
        'failed_no_object': 0,
        'failed_wrong_object': 0,
        'failed_error': 0
    }

    for i, parquet_path in enumerate(parquet_files):
        print(f"\n--- Processing file {i+1}/{len(parquet_files)} ---")
        file_stats = process_parquet_file(parquet_path, filter_obj, output_dir)

        # Update total statistics
        for key in total_stats:
            total_stats[key] += file_stats[key]

        print(f"File stats: {file_stats}")

        # Force garbage collection after each file
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

    # Print final summary
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total items processed: {total_stats['total']}")
    print(f"Passed robust filtering: {total_stats['passed']} ({total_stats['passed']/total_stats['total']*100:.1f}%)")
    print(f"Failed quality check: {total_stats['failed_quality']} ({total_stats['failed_quality']/total_stats['total']*100:.1f}%)")
    print(f"Failed no object: {total_stats['failed_no_object']} ({total_stats['failed_no_object']/total_stats['total']*100:.1f}%)")
    print(f"Failed wrong object: {total_stats['failed_wrong_object']} ({total_stats['failed_wrong_object']/total_stats['total']*100:.1f}%)")
    print(f"Failed other errors: {total_stats['failed_error']} ({total_stats['failed_error']/total_stats['total']*100:.1f}%)")
    print(f"\nFiltered files saved in: {output_dir}")

if __name__ == "__main__":
    main()