import tools.html_to_markdown as h2m
import os
import re


def batch_html_to_markdown_save_source(input_root_dir, out_root_dir, old_extension, new_extension, body_width, encoding='utf-8'):
    if (not os.path.exists(out_root_dir)):
        os.makedirs(out_root_dir)
    list_dirs = os.walk(input_root_dir)
    replace_reg = re.compile(old_extension + r'$')
    for root, dirs, files in list_dirs:
        for file_name in files:
            input_file_full_path = os.path.join(root, file_name)
            out_dir = root.replace(input_root_dir, out_root_dir, 1)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            output_file_full_path = os.path.join(out_dir, replace_reg.sub(new_extension, file_name))
            if (os.path.exists(output_file_full_path)):
                continue
            h2m.html_to_text_by_path(input_file_full_path, output_file_full_path, body_width, encoding)
