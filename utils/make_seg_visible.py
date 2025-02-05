'''
This script makes nnunet predictions visible by rescaling them to the full 8-bit 
range.

Author: Arthur Boschet
Modified by Armand Collin to use openCV instead of PIL
'''

import argparse
import os

import numpy as np
import cv2

def make_segmentations_visible(input_dir: str, output_dir: str) -> None:
    """
    Map segmentation values to make them visible in the output images by scaling them between 0 and 255.

    Parameters
    ----------
    input_dir : str
        The directory containing segmentation images.
    output_dir : str
        The directory to save mapped segmentation images.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):  # Assuming the segmentations are in PNG format
            file_path = os.path.join(input_dir, filename)
            # Open the image
            img_array = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            # Utilize broadcasting to avoid explicit looping for mapping
            min_label, max_label = img_array.min(), img_array.max()
            # Normalize the image array to 0-255 range
            img_mapped_array = ((img_array - min_label) * (255.0 / (max_label - min_label))).astype(np.uint8)
            # Convert numpy array back to image
            cv2.imwrite(os.path.join(output_dir, filename), img_mapped_array)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Map segmentation values and save to output directory.")
    parser.add_argument("input_dir", type=str, help="Directory containing segmentation images.")
    parser.add_argument("output_dir", type=str, help="Directory to save mapped segmentation images.")
    args = parser.parse_args()

    make_segmentations_visible(args.input_dir, args.output_dir)