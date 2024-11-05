'''nnunet dataset parsing
Read nnunet raw dataset, then convert it to a usable format. Requires a json 
file with the matching between nnunet's case-ID and the original filename i.e.
    {
        "001": "fname_1",
        "002": "fname_2",
        ...
        "036": "fname_36",
    }
Subject will be extracted from the original filenames

Author: Armand Collin
'''
import argparse
import json
import shutil
import cv2

from pathlib import Path

def main(datapath: Path, jsonpath: Path):
    # Load the case-ID to filename JSON file
    with open(jsonpath, "r") as f:
        case_id_to_fname = json.load(f)
    
    output_dir = Path('.') / "converted_data"
    output_dir.mkdir(exist_ok=True)

    training_files = datapath / "nnUNet_raw" / "Dataset011_CARS_BRAIN" / "imagesTr"
    subjects = set()
    for fname in training_files.glob("*.png"):
        # nnunet fnames have the following form: 
        #       CARS_BRAIN_XXX_0000.png where XXX is the case-id
        case_id = fname.stem.split("_")[2]
        subject_fname = case_id_to_fname[case_id]
        # original fnames have to following form:
        #       DATE-SUBJECTID-something-something-something.png
        subject_id = subject_fname.split("-")[1]
        subjects.add(subject_id)

        output_dir_subject = output_dir / subject_id
        output_dir_subject.mkdir(exist_ok=True)

        # Copy the image to the output directory
        output_fname = output_dir_subject / str(subject_fname)
        shutil.copy(fname, output_fname)

        label_fname = fname.parent.parent / "labelsTr" / f"CARS_BRAIN_{case_id}.png"
        output_label_fname = str(output_fname).replace(".png", "_seg-axonmyelin.png")
        raw_label = cv2.imread(str(label_fname), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(str(output_label_fname), 127*raw_label)

    print(f"Conversion done for subjects {subjects}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert nnunet dataset to usable format")
    parser.add_argument("datapath", type=Path, help="Path to the nnunet dataset")
    parser.add_argument("jsonpath", type=Path, help="Path to the case-ID to filename JSON file")
    args = parser.parse_args()

    main(args.datapath, args.jsonpath)