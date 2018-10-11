import os
import shutil


def file_extraction_by_suffix(input_dir, output_dir, suffix_content):
    list_dirs = os.walk(input_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            if f.endswith(suffix_content):
                input_file_path = os.path.join(root, f)
                output_file_path = os.path.join(output_dir, f)
                shutil.copy(input_file_path, output_file_path)
