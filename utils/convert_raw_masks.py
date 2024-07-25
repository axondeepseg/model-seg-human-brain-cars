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
    parser.add_argument("--dir",    default=None,   type=Path, help="Path to a directory containing masks.")
    parser.add_argument("--axon",   default=None,   type=Path, help="Path to the axon mask")
    parser.add_argument("--myelin", default=None,   type=Path, help="Path to the myelin mask")
    parser.add_argument("--output", default=None,   type=Path, help="Path to the output mask")
    args = parser.parse_args()

    if args.dir and (args.axon or args.myelin or args.output):
        raise ValueError("Please use either --dir or [--axon, --myelin and --output], not both.")

    # batch mode
    if args.dir:
        # get all pairs of axon/myelin masks
        all_masks = list(Path(args.dir).glob("*_seg-*.png"))
        valid_fnames = set([m.name.split("_seg-")[0] for m in all_masks])
        for fname in valid_fnames:
            axon = Path(args.dir) / f"{fname}_seg-axon.png"
            myelin = Path(args.dir) / f"{fname}_seg-myelin.png"
            output = Path(args.dir) / f"{fname}_nnunet-label.png"
            try:
                convert_raw_masks(str(axon), str(myelin), str(output))
            except Exception as e:
                print(f"Error processing {fname}: {e}")

    else:
        convert_raw_masks(str(args.axon), str(args.myelin), str(args.output))