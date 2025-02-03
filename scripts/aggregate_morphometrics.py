'''Aggregates morphometrics from every subject in a single csv file. The expected 
format for the input directory is the following:
input_dir
│
└───subject_1
│   │   subject_1_1.xlsx
│   │   subject_1_2.xlsx
│   │   ...
│
└───subject_2
│   │   ...
│
└───...
│
└───subject_n
│   │   ...
'''

import pandas as pd
import argparse
from pathlib import Path
import cv2


BALASANA_PX_SIZE = 0.167 # um/px


def get_image_size(img_path: Path):
    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    return img.shape

def get_total_subject_area(subject_dir: Path):
    '''Returns total area in um^2'''
    files = [x for x in subject_dir.glob("*_seg-axonmyelin.png")]
    total_area = 0
    for f in files:
        shape = get_image_size(f)
        total_area += shape[0] * shape[1] * BALASANA_PX_SIZE**2
    return total_area

def main(input_dir: Path, area: bool = False):
    subjects = [x.stem for x in input_dir.glob("*") if x.is_dir()]
    aggregated_df = pd.DataFrame()
    if area:
        area_df = pd.DataFrame(columns=["subject", "total_area"])
    for sub in subjects:
        target_dir = input_dir / sub
        files = [x for x in target_dir.glob("*axon_morphometrics.xlsx")]
        for f in files:
            df = pd.read_excel(f)
            df["subject"] = sub
            aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
        if area:
            total_area = get_total_subject_area(target_dir)
            area_df = pd.concat([area_df, pd.DataFrame({"subject": [sub], "total_area": [total_area]})], ignore_index=True)
    fname = input_dir / "aggregated_morphometrics.csv"
    aggregated_df.to_csv(fname, index=False)
    
    if area:
        fname_area = input_dir / "total_area.csv"
        area_df.to_csv(fname_area, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate morphometrics from every subject in a single csv file")
    parser.add_argument("input_dir", type=Path, help="Path to the directory containing the morphometrics files")
    parser.add_argument("-a", "--area", action='store_true' , help="Also computes total imaged area per subject.")
    args = parser.parse_args()

    main(args.input_dir, args.area)