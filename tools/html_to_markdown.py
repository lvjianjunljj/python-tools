# Author:Jianjun Lv
# Function: convert html to md

import html2text as ht  # pip install html2text


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
