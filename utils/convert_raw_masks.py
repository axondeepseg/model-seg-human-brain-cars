'''
Converts 2 8-bit binary masks (axon and myelin) into a single 8-bit mask with 
3 classes (background, axon, myelin) with values resp. 0, 1 and 2. This target 
format is what nnUNet expects.
'''

import argparse
from pathlib import Path

import cv2

def convert_raw_masks(axon_path, myelin_path, output_path):
    '''
    Converts 2 8-bit binary masks (axon and myelin) into a single axonmyelin 
    mask ready for nnunet training.

    Parameters
    ----------
    axon_path : str
        Path to the axon mask
    myelin_path : str
        Path to the myelin mask
    output_path : str
        Path to the output mask which will dictate its filename
    '''
    axon = cv2.imread(axon_path, cv2.IMREAD_GRAYSCALE) > 127
    myelin = cv2.imread(myelin_path, cv2.IMREAD_GRAYSCALE) > 127

    assert axon.shape == myelin.shape, "Axon and myelin masks must have the same shape"

    mask = axon.copy().fill(0)
    mask[axon] = 1
    mask[myelin] = 2

    cv2.imwrite(output_path, mask)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axon", type=Path, help="Path to the axon mask")
    parser.add_argument("--myelin", type=Path, help="Path to the myelin mask")
    parser.add_argument("--output", type=Path, help="Path to the output mask")
    args = parser.parse_args()

    convert_raw_masks(args.axon, args.myelin, args.output)