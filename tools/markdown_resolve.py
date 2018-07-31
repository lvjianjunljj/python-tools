import os
import subprocess

def batch_remove_table_extra_line_break(input_root_dir, encoding):
    list_dirs = os.walk(input_root_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            input_file_full_path = os.path.join(root, f)
            md_file = open(input_file_full_path, 'r', encoding=encoding, errors='ignore')
            text = md_file.read()
            if text.__contains__('---|---|---'):
                if text.__contains__('|\n') or text.__contains__('\n|'):
                    text = text.replace('|\n', '|').replace('\n|', '|')
                    open(input_file_full_path, "w", encoding=encoding).write(text)


def batch_latex_to_embedded_html(input_root_dir):
    list_dirs = os.walk(input_root_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            input_file_full_path = os.path.join(root, f)
            cmd = r'node generate_latex.js -i "' + input_file_full_path + r'" -o "' + input_file_full_path + r'"'
            subprocess.call(cmd, shell=True)