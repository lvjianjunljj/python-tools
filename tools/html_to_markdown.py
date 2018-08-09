import html2text as ht  # pip install html2text
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
            html_to_text_by_path(input_file_full_path, output_file_full_path, body_width, encoding)


def html_to_text_by_path(input_path, output_path, body_width, encoding='UTF-8'):
    text_maker = ht.HTML2Text()
    # text_maker.ignore_links = True
    text_maker.bypass_tables = False
    text_maker.body_width = body_width
    html_file = open(input_path, 'r', encoding=encoding, errors='ignore')
    html_page = html_file.read()
    for i in range(10):
        html_page = html_page.replace(r'<h' + str(10 - i), r'<h' + str(11 - i))
        html_page = html_page.replace(r'</h' + str(10 - i) + r'>', r'</h' + str(11 - i) + r'>')
    text = text_maker.handle(html_page)
    open(output_path, "w", encoding=encoding).write(text)  # write file as a md file


def html_to_text_by_content(input_content):
    text_maker = ht.HTML2Text()
    # text_maker.ignore_links = True
    text_maker.bypass_tables = False
    # path ="D:\\1.html"
    return text_maker.handle(input_content)
