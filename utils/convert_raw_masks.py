'''
Converts 2 8-bit binary masks (axon and myelin) into a single 8-bit mask with 
3 classes (background, myelin, axon) with values resp. 0, 1 and 2. This target 
format is what nnUNet expects.
'''

import argparse
from pathlib import Path

import cv2
import numpy as np

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
    axon = cv2.imread(axon_path, cv2.IMREAD_GRAYSCALE)
    myelin = cv2.imread(myelin_path, cv2.IMREAD_GRAYSCALE)

    assert axon.shape == myelin.shape, "Axon and myelin masks must have the same shape"
    assert len(np.unique(axon)) == 2, "Axon mask must be binary"
    assert len(np.unique(myelin)) == 2, "Myelin mask must be binary"

    mask = axon.copy()
    mask.fill(0)
    mask[myelin >= 127] = 1
    mask[axon >= 127] = 2

    cv2.imwrite(output_path, mask)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--axon", type=Path, help="Path to the axon mask")
    parser.add_argument("--myelin", type=Path, help="Path to the myelin mask")
    parser.add_argument("--output", type=Path, help="Path to the output mask")
    args = parser.parse_args()

    convert_raw_masks(str(args.axon), str(args.myelin), str(args.output))