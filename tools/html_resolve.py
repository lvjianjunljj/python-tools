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


def get_element_string_by_class_attribute_first(htmlContent, attribute_value, label_name=''):
    soup = BeautifulSoup(htmlContent, 'html5lib')
    all_elements = soup.select((str)(label_name + r'.' + attribute_value).replace(' ', '.'))
    if all_elements.__len__() > 0:
        return str(all_elements[0])
    else:
        return ''


def get_simple_tf_content_contains_time(html_content):
    tf_simple_start_content = r'<h1 itemprop="name" class="devsite-page-title">';
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

def create_dir_by_tf_python_api_strecture(html_content, root_dir_path, encoding):
    soup = BeautifulSoup(html_content, 'html5lib')
    root_element = soup.select('ul')[0]
    dfs_create_tf_python_dir(root_element, root_dir_path, encoding)


def dfs_create_tf_python_dir(curElement, dir_path, encoding):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    children_element = curElement.children
    for child_element in children_element:
        next_children_element = child_element.children
        count = 0
        next_child_0 = None
        next_child_2 = None
        while count < 3:
            try:
                if count == 0:
                    next_child_0 = next_children_element.__next__()
                elif count == 2:
                    next_child_2 = next_children_element.__next__()
                else:
                    next_children_element.__next__()
                count += 1
            except StopIteration:
                break
        if count == 1:
            file_path = os.path.join(dir_path, next_child_0.text + ".html")
            if os.path.exists(file_path):
                continue
            href = next_child_0['href']
            html_content = crawler.crawl(href)
            tf_content = get_simple_tf_content_contains_time(html_content)
            if tf_content == '':
                print(r'crawl url"' + href + r'" has error...')
                print(r'file path is: ' + file_path)
            else:
                open(file_path, "w", encoding=encoding).write(tf_content)
        else:
            dfs_create_tf_python_dir(next_child_2, os.path.join(dir_path, next_child_0.text), encoding)


def create_dir_by_keras_api_strecture(keras_root_url, html_content, root_dir_path, encoding,
                                      download_expanded_label=False):
    soup = BeautifulSoup(html_content, 'html5lib')
    root_element = soup.select('ul')[0]
    for element in root_element.children:
        try:
            children_element = element.children
        except AttributeError:
            continue
        count = 0
        child_element_0 = None
        child_element_1 = None
        child_element_2 = None
        while count < 3:
            try:
                if count == 0:
                    child_element_0 = children_element.__next__()
                    if str(child_element_0).replace(' ', '').replace('\n', '') == '':
                        continue
                elif count == 1:
                    child_element_1 = children_element.__next__()
                    if str(child_element_1).replace(' ', '').replace('\n', '') == '':
                        continue
                else:
                    child_element_2 = children_element.__next__()
                    if str(child_element_2).replace(' ', '').replace('\n', '') == '':
                        continue
                count += 1
            except StopIteration:
                break
        if count == 0:
            continue
        elif count == 1:
            next_level_element_list = None
            try:
                next_level_element_list = BeautifulSoup(str(child_element_0), 'html5lib').select('ul')
                # next_level_element_list = child_element_0.select('ul')
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
                        crawl_keras_data_to_local(file_path, href, encoding)
            else:

                file_path = os.path.join(root_dir_path, child_element_0.text.strip() + ".html")
                href = keras_root_url + child_element_0['href']
                crawl_keras_data_to_local(file_path, href, encoding)

        else:
            # Currently expanded label
            file_path = os.path.join(root_dir_path, child_element_0.text + ".html")
            href = keras_root_url + child_element_0['href']
            crawl_keras_data_to_local(file_path, href, encoding)
            if download_expanded_label:
                print(download_expanded_label)


def crawl_keras_data_to_local(file_path, href, encoding):
    file_path = file_path.replace('\n', '')
    if os.path.exists(file_path):
        return
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    html_content = crawler.crawl(href)
    keras_content = get_keras_content(html_content)
    if keras_content == '':
        print(r'crawl url"' + href + r'" has error...')
        print(r'file path is: ' + file_path)
    else:
        open(file_path, "w", encoding=encoding).write(keras_content)


def create_dir_by_pytorch_api_strecture(pytorch_root_url, html_content, root_dir_path, encoding):
    soup = BeautifulSoup(html_content, 'html5lib')
    root_elements = soup.select('div')[0].children
    span_name = None
    for root_element in root_elements:
        try:
            temp =  root_element['class']
            span_name = root_element.text
        except TypeError:
            continue
        except KeyError:
            dfs_create_pytorch_dir(pytorch_root_url, root_element, os.path.join(root_dir_path, span_name), 1, 1, encoding)




def dfs_create_pytorch_dir(pytorch_root_url, cur_element, dir_path, cur_depth, max_depth, encoding):
    if cur_depth > max_depth:
        return
    for child_element in cur_element.children:
        try:
            next_children_element = child_element.children
        except AttributeError:
            continue
        count = 0
        next_child_element_0 = None
        next_child_element_1 = None
        while count < 2:
            try:
                if count == 0:
                    next_child_element_0 = next_children_element.__next__()
                    if str(next_child_element_0).replace(' ', '').replace('\n', '') == '':
                        continue
                else:
                    next_child_element_1 = next_children_element.__next__()
                    if str(next_child_element_1).replace(' ', '').replace('\n', '') == '':
                        continue
                count += 1
            except StopIteration:
                break
        if count > 1:
            dfs_create_pytorch_dir(pytorch_root_url, next_child_element_1,
                                   os.path.join(dir_path, make_file_path_legal(next_child_element_0.text,'_')), cur_depth + 1, max_depth, encoding)
        file_path = os.path.join(dir_path, make_file_path_legal(next_child_element_0.text, "_") + ".html")
        if (os.path.exists(file_path)):
            continue
        href = pytorch_root_url + next_child_element_0["href"]
        htmlContent = crawler.crawl(href)
        keras_content = get_pytorch_content(htmlContent)
        if (keras_content == ""):
            print(r'crawl url"' + href + r'" has error...')
            print("file path is: " + file_path)
        else:
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            open(file_path, "w", encoding=encoding).write(keras_content)


def make_file_path_legal(path_str, replace_str):
    return path_str.replace('\\', replace_str). \
        replace('/', replace_str). \
        replace(':', replace_str). \
        replace('*', replace_str). \
        replace('?', replace_str). \
        replace('<', replace_str). \
        replace('>', replace_str). \
        replace('|', replace_str)
