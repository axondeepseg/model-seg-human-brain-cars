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


def main(input_dir: Path):
    subjects = [x.stem for x in input_dir.glob("*") if x.is_dir()]
    aggregated_df = pd.DataFrame()
    for sub in subjects:
        target_dir = input_dir / sub
        files = [x for x in target_dir.glob("*axon_morphometrics.xlsx")]
        for f in files:
            df = pd.read_excel(f)
            df["subject"] = sub
            aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
    fname = input_dir / "aggregated_morphometrics.csv"
    aggregated_df.to_csv(fname, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate morphometrics from every subject in a single csv file")
    parser.add_argument("input_dir", type=Path, help="Path to the directory containing the morphometrics files")
    args = parser.parse_args()

    main(args.input_dir)