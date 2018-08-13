import os
import subprocess
import platform
import urllib.request
import re

def batch_latex_to_embedded_html(input_root_dir):
    system_name = platform.system()
    list_dirs = os.walk(input_root_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            input_file_full_path = os.path.join(root, f)
            cmd = r'node generate_latex.js -i "' + input_file_full_path + r'" -o "' + input_file_full_path
            if system_name == "Windows":
                cmd += r'">nul'
                # if you use PowerShell
                # cmd += r'">$null'
            elif system_name == "Linux":
                cmd += r'">/dev/null'
            else:
                # other system
                cmd += r'"'
            subprocess.call(cmd, shell=True)


def batch_clean_title(root_dir, encoding):
    list_dirs = os.walk(root_dir)
    for root, dirs, files in list_dirs:
        for file_name in files:
            if not file_name.endswith(r'.md'):
                continue
            input_file_full_path = os.path.join(root, file_name)
            markdown_file = open(input_file_full_path, 'r', encoding=encoding, errors='ignore')
            line = markdown_file.readline()
            regular_expression = r'\[.*?\]\(.*?\)'
            write_content = ''
            while line:
                if line.startswith(r'##'):
                    try:
                        search_res = re.search(regular_expression, line).span()
                        start_index = search_res[0] + 1
                        end_index = search_res[0]
                        buckets_difference = 1
                        while buckets_difference > 0:
                            end_index += 1
                            if line[end_index] == '[':
                                buckets_difference += 1
                            elif line[end_index] == ']':
                                buckets_difference -= 1
                        line = line[0:start_index - 1] + line[start_index:end_index]
                    except AttributeError:
                        pass
                write_content += line
                line = markdown_file.readline()
            open(input_file_full_path, "w", encoding=encoding).write(write_content)


# Convert internal links to document relative addresses
def internal_links_convert(root_dir, framework_name, href_path_dict, encoding):
    framework_dir = os.path.join(root_dir, framework_name)
    start_content = r'(http'

    list_dirs = os.walk(framework_dir)
    for root, dirs, files in list_dirs:
        for file_name in files:
            if not file_name.endswith(r'.md'):
                continue
            input_file_full_path = os.path.join(root, file_name)
            markdown_file = open(input_file_full_path, 'r', encoding=encoding, errors='ignore')
            markdown_content = markdown_file.read()
            res_markdown_content = ''
            end_index = 0
            try:
                while True:
                    start_index = markdown_content.index(start_content, end_index)
                    res_markdown_content += markdown_content[end_index:start_index + 1]
                    brackets_difference_count = 1
                    end_index = start_index
                    while brackets_difference_count > 0:
                        end_index += 1
                        if markdown_content[end_index] == r'(':
                            brackets_difference_count += 1
                        elif markdown_content[end_index] == r')':
                            brackets_difference_count -= 1

                    if framework_name == r'TensorFlow':
                        res_markdown_content += tensor_flow_internal_links_convert(framework_name,
                                                                                   href_path_dict,
                                                                                   markdown_content[
                                                                                   start_index + 1:end_index])
                    elif framework_name == r'Keras':
                        res_markdown_content += keras_internal_links_convert(framework_name,
                                                                             href_path_dict,
                                                                             markdown_content[
                                                                             start_index + 1:end_index])
                    else:
                        res_markdown_content += pytorch_internal_links_convert(framework_name,
                                                                               href_path_dict,
                                                                               markdown_content[
                                                                               start_index + 1:end_index])
            except ValueError:
                res_markdown_content += markdown_content[end_index:markdown_content.__len__()]
                pass
            open(input_file_full_path, "w", encoding=encoding).write(res_markdown_content)


# the old_link does not contain brackets
# the process in Comment section is to find the file location based on the link, it lists all the possible path by
# Bit operation, but it is not suitable for Keras, so I save all the correspondence of href and path in a dict

# def tensor_flow_internal_links_convert(root_dir, framework_name, tf_root_url, old_link):
#     relative_link = old_link[tf_root_url.__len__():old_link.__len__()]
#     last_title_content = None
#     try:
#         mark_index = relative_link.index(r'#')
#         last_title_content = relative_link[mark_index + 1:relative_link.__len__()]
#         relative_link = relative_link[0:mark_index]
#     except ValueError:
#         pass
#     split_cube = relative_link.split('/')
#     res_path = None
#
#     for i in range(int(math.pow(2, split_cube.__len__() - 1))):
#         binary_str = ('{0:0' + str(split_cube.__len__() - 1) + 'b}').format(i)
#         relative_file_path = split_cube[0]
#         for j in range(split_cube.__len__() - 1):
#             if binary_str[j] == '0':
#                 relative_file_path += r'.' + split_cube[j + 1]
#             else:
#                 relative_file_path = os.path.join(relative_file_path, split_cube[j + 1])
#
#         absolute_file_path = os.path.join(root_dir, framework_name, relative_file_path)
#         if os.path.exists(os.path.join(absolute_file_path, r'Overview r1.9.md')):
#             res_path = os.path.join(framework_name, relative_file_path, r'Overview r1.9')
#             break
#         elif os.path.exists(os.path.join(absolute_file_path, r'Overview.md')):
#             res_path = os.path.join(framework_name, relative_file_path, r'Overview')
#             break
#         elif os.path.exists(absolute_file_path + r'.md'):
#             res_path = os.path.join(framework_name, relative_file_path)
#             break
#     if res_path == None:
#         # if cannot find the relative file path, we think of it as an external link, save it as before and process it later in external_links_convert function
#         print(old_link)
#         return old_link
#     return res_path + ('' if last_title_content == None else r'?id=' + last_title_content)
def tensor_flow_internal_links_convert(framework_name, href_path_dict, old_link):
    last_title_content = None
    index_link = old_link
    try:
        mark_index = old_link.index(r'#')
        last_title_content = old_link[mark_index + 1:old_link.__len__()]
        index_link = old_link[0:mark_index]
    except ValueError:
        pass
    try:
        res_path = urllib.request.quote(href_path_dict[index_link])
        # Minus three is to eliminate the point and extension name 'md'
        return framework_name + r'/' + res_path[0:res_path.__len__() - 3] + (
            '' if last_title_content == None else r'?id=' + last_title_content)
    except KeyError:
        # if cannot find the relative file path, we think of it as an external link,
        # save it as before and process it later in external_links_convert function
        return old_link


def keras_internal_links_convert(framework_name, href_path_dict, old_link):
    # very hard code, so ugly
    old_link = old_link.replace(r'https://keras.io/../../', r'https://keras.io/').replace(
        r'https://keras.io/../', r'https://keras.io/').replace(r'https://keras.io/..', r'https://keras.io/.')
    last_title_content = None
    index_link = old_link
    try:
        mark_index = old_link.index(r'#')
        last_title_content = old_link[mark_index:old_link.__len__()]
        index_link = old_link[0:mark_index]
    except ValueError:
        try:

            mark_index = old_link.index(r' "')
            last_title_content = old_link[mark_index:old_link.__len__()]
            index_link = old_link[0:mark_index]
        except ValueError:
            pass
    if not index_link.endswith(r'/') and not index_link.endswith(r'.'):
        index_link += r'/'
    try:
        res_path = href_path_dict[index_link]
        # Minus three is to eliminate the point and extension name 'md'
        return framework_name + r'/' + res_path[0:res_path.__len__() - 3] + ('' if last_title_content == None else (
                r'?id=' + last_title_content[1:last_title_content.__len__()]) if last_title_content.startswith(
            r'#') else last_title_content)
    except KeyError:
        matching_href = keras_get_matching_href(href_path_dict.keys(), index_link)
        if matching_href == '':
            return old_link
        else:
            res_path = urllib.request.quote(href_path_dict[matching_href])
            # Minus three is to eliminate the point and extension name 'md'
            return framework_name + r'/' + res_path[0:res_path.__len__() - 3] + ('' if last_title_content == None else (
                    r'?id=' + last_title_content[1:last_title_content.__len__()]) if last_title_content.startswith(
                r'#') else last_title_content)


def keras_get_matching_href(href_list, index_link):
    split_cube = index_link.split(r'/')
    index_last_part = split_cube[split_cube.__len__() - 2] + r'/'
    for href in href_list:
        if href.endswith(index_last_part):
            return href
    return ''


def pytorch_internal_links_convert(framework_name, href_path_dict, old_link):
    # very hard code, so ugly
    old_link = old_link.replace(r'https://pytorch.org/docs/stable/../', r'https://pytorch.org/docs/stable/')
    last_title_content = None
    index_link = old_link
    try:
        mark_index = old_link.index(r'#')
        last_title_content = old_link[mark_index + 1:old_link.__len__()]
        index_link = old_link[0:mark_index]
    except ValueError:
        pass
    try:
        res_path = urllib.request.quote(href_path_dict[index_link])
        # Minus three is to eliminate the point and extension name 'md'
        return framework_name + r'/' + res_path[0:res_path.__len__() - 3] + (
            '' if last_title_content == None else r'?id=' + last_title_content)
    except KeyError:
        return old_link


def batch_external_links_convert(root_dir, encoding):
    list_dirs = os.walk(root_dir)
    index_content = r'](http'
    for root, dirs, files in list_dirs:
        for file_name in files:
            if not file_name.endswith(r'.md'):
                continue
            input_file_full_path = os.path.join(root, file_name)
            markdown_file = open(input_file_full_path, 'r', encoding=encoding, errors='ignore')
            markdown_content = markdown_file.read()
            # we should get the string like [[example]](https://exaple)
            # and also eliminate the first [example] in string [example][example](https://exaple)
            # so we discard the use of regular expressions and use count difference between left bracket and right bracket
            # regular_expression = r'\[[^[\]]*?\]\(https{0,1}://.*?\)'
            # end_index = 0
            # res_markdown_content = ''
            # try:
            #     while True:
            #         search_res = re.search(regular_expression, markdown_content[end_index:]).span()
            #         start_index = search_res[0] + end_index
            #         res_markdown_content += markdown_content[end_index:start_index]
            #         end_index += search_res[1]
            #         res_markdown_content += external_links_convert(markdown_content[start_index:end_index])
            #
            # except AttributeError:
            #     res_markdown_content += markdown_content[end_index:]
            #     pass
            end_index = 0
            res_markdown_content = ''
            try:
                # pay attention to the difference of the Initial and final values of index for each cycle with internal
                # the old_link parameter of internal links convert does not contain brackets
                # but the old_link parameter of external links convert contain brackets
                while True:
                    index = markdown_content.index(index_content, end_index)
                    start_index = index
                    brackets_difference_count = 1
                    while brackets_difference_count > 0:
                        start_index -= 1
                        if markdown_content[start_index] == r']':
                            brackets_difference_count += 1
                        elif markdown_content[start_index] == r'[':
                            brackets_difference_count -= 1
                    res_markdown_content += markdown_content[end_index:start_index]
                    brackets_difference_count = 1
                    end_index = index + 2
                    while brackets_difference_count > 0:
                        if markdown_content[end_index] == r'(':
                            brackets_difference_count += 1
                        elif markdown_content[end_index] == r')':
                            brackets_difference_count -= 1
                        end_index += 1
                    res_markdown_content += external_links_convert(markdown_content[start_index:end_index])
            except ValueError:
                res_markdown_content += markdown_content[end_index:markdown_content.__len__()]
                pass
            except IndexError:
                print('file "{0}" has error in external links convert'.format('test'))
                pass
            open(input_file_full_path, "w", encoding=encoding).write(res_markdown_content)


def external_links_convert(md_input_content):
    index = md_input_content.index('](http')
    button_content = md_input_content[1:index]
    link = md_input_content[index + 2:md_input_content.__len__() - 1]
    # not do anything with the link to the image
    if link.lower().endswith('png') or link.lower().endswith('bmp') or link.lower().endswith('gif') \
            or link.lower().endswith('jpeg') or link.lower().endswith('jpg') or link.lower().endswith('tiff') \
            or link.lower().endswith('psd'):
        return md_input_content
    # TO DO, it cost much time to confirm the availability of the link by http post
    # link_content = crawler.crawl(link)
    # if link_content == '':
    #     return button_content
    # else:
    on_click_content = escape_html(r'vscodeai_open(\'{0}\')'.format(link))
    return r'<a onClick="{1}" style="cursor: pointer">{0}</a>'.format(button_content, on_click_content)


def escape_html(unsafe_content):
    return unsafe_content.replace(r'&', '&amp;'). \
        replace(r'<', '&lt;'). \
        replace(r'>', '&gt;'). \
        replace(r'"', '&quot;'). \
        replace(r'\'', '&#039;')
