#!/usr/bin/env python3

"""
Test script to run robust filtering on a single parquet file
"""

import os
from robust_filter import RobustImageFilter, process_parquet_file

def main():
    """Test the robust filtering on first parquet file"""
    # Initialize the filter
    print("Initializing robust image filter...")
    filter_obj = RobustImageFilter()

    # Test on first parquet file
    input_file = "3dgen_filtered_parquets/filtered_dataset_0000.parquet"
    output_dir = "3dgen_robust_filtered_test"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing {input_file}...")
    stats = process_parquet_file(input_file, filter_obj, output_dir)

    print(f"\n=== RESULTS ===")
    print(f"Total items: {stats['total']}")
    print(f"Passed: {stats['passed']} ({stats['passed']/stats['total']*100:.1f}%)")
    print(f"Failed quality: {stats['failed_quality']}")
    print(f"Failed no object: {stats['failed_no_object']}")
    print(f"Failed wrong object: {stats['failed_wrong_object']}")
    print(f"Failed other: {stats['failed_error']}")
    print(f"\nOutput saved to: {output_dir}")

if __name__ == "__main__":
    main()