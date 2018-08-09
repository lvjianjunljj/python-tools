from bs4 import BeautifulSoup
import os
import tools.crawler as crawler


def push_h_down_one_level(html_content, max_h_level=10):
    for i in range(max_h_level):
        html_content = html_content.replace(r'<h' + str(max_h_level - i), r'<h' + str(max_h_level + 1 - i))
        html_content = html_content.replace(r'</h' + str(max_h_level - i) + r'>',
                                            r'</h' + str(max_h_level + 1 - i) + r'>')
    return html_content


def delete_code_label_in_h(html_content, max_h_level=10):
    h_list = []
    for i in range(max_h_level):
        h_list.append('h' + str(i + 1))
    soup = BeautifulSoup(html_content, 'html5lib')
    children_h = soup.find_all(h_list)
    for child_h in children_h:
        if child_h != None and child_h.string != None:
            child_h.string = child_h.string.replace('<code>', '').replace('</code>', '')
    return str(soup)


def address_relative_to_absolute(html_content, root_url):
    soup = BeautifulSoup(html_content, 'html5lib')
    descendants = soup.descendants
    for descendant in descendants:
        try:
            href = descendant['href']
            if not href.startswith('http'):
                if href.startswith(r'/'):
                    href = href[1:href.__len__()]
                descendant['href'] = root_url + href
        except TypeError:
            pass
        except KeyError:
            pass
        try:
            src = descendant['src']
            if not src.startswith('http'):
                if src.startswith(r'/'):
                    src = src[1:src.__len__()]
                descendant['src'] = root_url + src
        except TypeError:
            pass
        except KeyError:
            pass
    return str(soup)


def del_attr_all(html_content, attr):
    soup = BeautifulSoup(html_content, 'html5lib')
    descendants = soup.descendants
    for descendant in descendants:
        try:
            del descendant[attr]
        except TypeError:
            pass
        except KeyError:
            pass
    return str(soup)


def del_content_with_mark(html_content, mark_str):
    soup = BeautifulSoup(html_content, 'html5lib')
    # label_list = soup.select(label_name)
    # for label_unit in label_list:
    #     for content in label_unit.contents:
    #         try:
    #             if content.text.replace(' ', '').replace('\n', '').replace('\t', '') == mark_str:
    #                 label_unit.contents.remove(content)
    #         except AttributeError:
    #             pass
    dfs_content_with_mark(soup, mark_str)
    return str(soup)


def dfs_content_with_mark(html_element, mark_str):
    for content in html_element.contents:
        try:
            if content.text.replace(' ', '').replace('\n', '').replace('\t', '') == mark_str:
                html_element.contents.remove(content)
            else:
                dfs_content_with_mark(content, mark_str)
        except AttributeError:
            pass


def get_element_string_by_class_attribute_first(html_content, attribute_value, label_name=''):
    soup = BeautifulSoup(html_content, 'html5lib')
    all_elements = soup.select((str)(label_name + r'.' + attribute_value).replace(' ', '.'))
    if all_elements.__len__() > 0:
        return str(all_elements[0])
    else:
        return ''


def get_simple_tf_content_contains_time(html_content):
    tf_simple_start_content = r'<h1 itemprop="name" class="devsite-page-title">'
    tf_simple_mid_content = r'<p class="devsite-content-footer-date" itemprop="datePublished"'
    tf_simple_end_content = r'</div>'
    try:
        start_index = html_content.index(tf_simple_start_content)
        mid_index = html_content.index(tf_simple_mid_content)
        end_index = html_content.index(tf_simple_end_content, mid_index)
        return delete_code_label_in_h(
            push_h_down_one_level(html_content[start_index:end_index] + tf_simple_end_content))
    except ValueError:
        return ''


def get_keras_content(html_content):
    keras_start_content = r'<div role="main">'
    keras_end_content = r'</footer>'
    try:
        start_index = html_content.index(keras_start_content)
        end_index = html_content.index(keras_end_content, start_index)
        return html_content[start_index:end_index] + keras_end_content
    except ValueError:
        return ''


def get_pytorch_content(html_content):
    pytorch_start_content = r'<div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">'
    pytorch_end_content = r'</footer>'
    start_index = html_content.index(pytorch_start_content)
    end_index = html_content.index(pytorch_end_content)
    return html_content[start_index:end_index] + pytorch_end_content


def create_dir_by_tf_python_api_strecture(tf_root_url, html_content, root_dir_path, tf_python_href_path_dict, encoding):
    soup = BeautifulSoup(html_content, 'html5lib')
    root_element = soup.select('ul')[0]
    dfs_create_tf_python_dir(tf_root_url, root_element, root_dir_path, tf_python_href_path_dict, encoding)


def dfs_create_tf_python_dir(tf_root_url, curElement, dir_path, tf_python_href_path_dict, encoding):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    children_element = curElement.children
    for child_element in children_element:
        next_children_element = child_element.contents
        if next_children_element.__len__() == 1:
            file_path = os.path.join(dir_path, next_children_element[0].text + ".html")
            href = next_children_element[0]['href']
            # if not file_path in tf_python_path_list:
            #     tf_python_path_list.append(file_path)
            # else:
            #     print(r'write to path_list has repeated data, file path i : "' + file_path + r'"')
            tf_python_href_path_dict[href] = file_path
            if os.path.exists(file_path):
                continue
            html_content = crawler.crawl(href, encoding)
            tf_content = get_simple_tf_content_contains_time(html_content)
            if tf_content == '':
                print(r'crawl url"' + href + r'" has error...')
                print(r'file path is: ' + file_path)
            else:
                open(file_path, "w", encoding=encoding).write(address_relative_to_absolute(tf_content, tf_root_url))
        else:
            dfs_create_tf_python_dir(tf_root_url, next_children_element[2],
                                     os.path.join(dir_path, next_children_element[0].text), tf_python_href_path_dict,
                                     encoding)


def create_dir_by_keras_api_strecture(keras_root_url, html_content, root_dir_path, keras_href_path_dict, encoding,
                                      download_expanded_label=False):
    soup = BeautifulSoup(html_content, 'html5lib')
    root_element = soup.select('ul')[0]
    for element in root_element.children:
        try:
            children_element = element.contents
        except AttributeError:
            continue
        for child_element in children_element:
            if child_element.replace(' ', '').replace('\n', '') == '':
                children_element.remove(child_element)
        if children_element.__len__() == 0:
            continue
        elif children_element.__len__() == 1:
            try:
                next_level_element_list = element.select('ul')
            except AttributeError:
                continue
            if next_level_element_list.__len__() > 0:
                li_element_list = next_level_element_list[0].children
                label_name = None
                for li_element in li_element_list:
                    if str(li_element).replace(' ', '').replace('\n', '') == '':
                        continue
                    if li_element.select("span").__len__() > 0:
                        label_name = li_element.text
                    else:
                        file_path = os.path.join(root_dir_path, label_name, li_element.text.strip() + ".html")
                        href = keras_root_url + li_element.select("a")[0]["href"]
                        crawl_keras_data_to_local(keras_root_url, file_path, href, keras_href_path_dict, encoding)
            else:

                file_path = os.path.join(root_dir_path, children_element[0].text.strip() + ".html")
                href = keras_root_url + children_element[0]['href']
                crawl_keras_data_to_local(keras_root_url, file_path, href, keras_href_path_dict, encoding)

        else:
            # Currently expanded label
            file_path = os.path.join(root_dir_path, children_element[0].text + ".html")
            href = keras_root_url + children_element[0]['href']
            crawl_keras_data_to_local(keras_root_url, file_path, href, keras_href_path_dict, encoding)
            if download_expanded_label:
                # TO DO
                print(download_expanded_label)


def crawl_keras_data_to_local(keras_root_url, file_path, href, keras_href_path_dict, encoding):
    file_path = file_path.replace('\n', '')
    # if not file_path in keras_path_list:
    #     keras_path_list.append(file_path)
    # else:
    #     print(r'write to path_list has repeated data, file path i : "' + file_path + r'"')
    keras_href_path_dict[href] = file_path
    if os.path.exists(file_path):
        return
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    html_content = crawler.crawl(href, encoding)
    keras_content = get_keras_content(html_content)
    if keras_content == '':
        print(r'crawl url"' + href + r'" has error...')
        print(r'file path is: ' + file_path)
    else:
        open(file_path, "w", encoding=encoding).write(address_relative_to_absolute(keras_content, keras_root_url))


def create_dir_by_pytorch_api_strecture(pytorch_root_url, html_content, root_dir_path, pytorch_href_path_dict,
                                        encoding):
    if not os.path.exists(root_dir_path):
        os.makedirs(root_dir_path)
    # Manually crawl the root url page
    htmlContent = crawler.crawl(pytorch_root_url, encoding)
    pytorch_content = get_pytorch_content(htmlContent)
    pytorch_home_page_file_path = os.path.join(root_dir_path, r'Home.html')
    pytorch_href_path_dict[pytorch_root_url] = pytorch_home_page_file_path
    open(pytorch_home_page_file_path, "w", encoding=encoding).write(del_content_with_mark(del_attr_all(
        address_relative_to_absolute(pytorch_content, pytorch_root_url), 'title'), '¶'))
    soup = BeautifulSoup(html_content, 'html5lib')
    root_elements = soup.select('div')[0].children
    span_name = None
    for root_element in root_elements:
        try:
            temp = root_element['class']
            span_name = root_element.text
        except TypeError:
            continue
        except KeyError:
            dfs_create_pytorch_dir(pytorch_root_url, root_element, os.path.join(root_dir_path, span_name), 1, 1,
                                   pytorch_href_path_dict, encoding)


def dfs_create_pytorch_dir(pytorch_root_url, cur_element, dir_path, cur_depth, max_depth, pytorch_href_path_dict,
                           encoding):
    if cur_depth > max_depth:
        return
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for child_element in cur_element.children:
        try:
            next_children_element = child_element.contents
        except AttributeError:
            # Skip blank content
            continue
        if next_children_element.__len__() > 1:
            dfs_create_pytorch_dir(pytorch_root_url, next_children_element[1],
                                   os.path.join(dir_path, make_file_path_legal(next_children_element[0].text, '_')),
                                   cur_depth + 1, max_depth,
                                   pytorch_href_path_dict, encoding)
        file_path = os.path.join(dir_path, make_file_path_legal(next_children_element[0].text, "_") + ".html")
        href = pytorch_root_url + next_children_element[0]["href"]
        # if not file_path in pytorch_path_list:
        #     pytorch_path_list.append(file_path)
        # else:
        #     print(r'write to path_list has repeated data, file path i : "' + file_path + r'"')
        pytorch_href_path_dict[href] = file_path
        if (os.path.exists(file_path)):
            continue
        htmlContent = crawler.crawl(href, encoding)
        pytorch_content = get_pytorch_content(htmlContent)
        if (pytorch_content == ""):
            print(r'crawl url"' + href + r'" has error...')
            print("file path is: " + file_path)
        else:
            open(file_path, "w", encoding=encoding).write(
                del_content_with_mark(
                    del_attr_all(address_relative_to_absolute(pytorch_content, pytorch_root_url), 'title'), '¶'))


def make_file_path_legal(path_str, replace_str):
    return path_str.replace('\\', replace_str). \
        replace('/', replace_str). \
        replace(':', replace_str). \
        replace('*', replace_str). \
        replace('?', replace_str). \
        replace('<', replace_str). \
        replace('>', replace_str). \
        replace('|', replace_str)
