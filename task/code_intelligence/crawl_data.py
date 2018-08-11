import tools.html_resolve as hr
from tools import crawler


def crawl_tensor_flow_python_tree_structure(tf_python_root_url, tf_python_root_dir, tf_python_href_path_dict, encoding='utf-8'):
    html_content = crawler.crawl(tf_python_root_url, encoding)
    nav_label_content = hr.get_element_string_by_class_attribute_first(html_content, r'devsite-section-nav devsite-nav nocontent')
    start_index_content = r'Python API r1.10</span>'
    end_index_content = r'<li class="devsite-nav-item devsite-nav-item-section-expandable devsite-nav-accordion">'
    start_index = nav_label_content.index(start_index_content)
    end_index = nav_label_content.index(end_index_content, start_index)
    # delete the label </li>
    intercepted_content = nav_label_content[start_index + start_index_content.__len__():
                                            end_index - 5]

    hr.create_dir_by_tf_python_api_strecture(tf_python_root_url, intercepted_content, tf_python_root_dir, tf_python_href_path_dict, encoding)


def crawl_keras_tree_structure(keras_root_url, keras_root_dir, keras_href_path_dict, encoding='utf-8'):
    html_content = crawler.crawl(keras_root_url, encoding)
    div_label_content = hr.get_element_string_by_class_attribute_first(html_content, r'wy-menu wy-menu-vertical')
    hr.create_dir_by_keras_api_strecture(keras_root_url, div_label_content, keras_root_dir, keras_href_path_dict, encoding)


def crawl_pytorch_tree_structure(pytorch_root_url, keras_root_dir, pytorch_href_path_dict, encoding='utf-8'):
    html_content = crawler.crawl(pytorch_root_url, encoding)
    div_label_content = hr.get_element_string_by_class_attribute_first(html_content, r'wy-menu wy-menu-vertical')
    hr.create_dir_by_pytorch_api_strecture(pytorch_root_url, div_label_content, keras_root_dir, pytorch_href_path_dict, encoding)
