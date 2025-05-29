'''
This script adds a suffix to every filename in the given directory; however, it 
preserves the original suffixes at the end of the filenames.
'''

__author__ = 'Armand Collin'

from pathlib import Path
import argparse


SUFFIX_TO_ADD = '_slice2'
SUFFIXES_TO_PRESERVE = [
    '_seg-axon.png',
    '_seg-myelin.png',
    '_seg-axonmyelin.png',
    '_axonmyelin_index.png',
    '_index.png',
    '_axon_morphometrics.xlsx',
]


def main(directory: str):
    directory_path = Path(directory)

    subjects = [f for f in directory_path.glob('*') if f.is_dir()]
    print(f'Found {len(subjects)} subjects.')

    for subject in subjects:
        files_to_rename = [
            f for f in subject.glob('*') if (f.name.endswith('.png') or f.name.endswith('.xlsx'))
        ]
        print(f'\tsub-{subject.name} -> {len(files_to_rename)} files to rename.')
        for file in files_to_rename:
            has_suffix = False
            # suffix order matters
            for suffix in SUFFIXES_TO_PRESERVE:
                if file.name.endswith(suffix):
                    new_name = file.name.replace(suffix, f'{SUFFIX_TO_ADD}{suffix}')
                    new_file_path = file.parent / new_name
                    file.rename(new_file_path)
                    
                    has_suffix = True
                    break
            if not has_suffix:
                # then it has to be an input image
                new_name = file.name.replace('.png', f'{SUFFIX_TO_ADD}.png')
                new_file_path = file.parent / new_name
                file.rename(new_file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a suffix to filenames in a directory.')
    parser.add_argument('directory', type=str, help='Directory containing the files to rename')
    args = parser.parse_args()

    main(args.directory)
    print(f"Suffix '{SUFFIX_TO_ADD}' added to filenames in '{args.directory}'.")