import sys

sys.path.append('../..')

import json
import os
import re
import shutil
import subprocess
import task.code_intelligence.crawl_data as crawler
import tools.batch_html_to_markdown as bh2m
import tools.file_compress as file_compress
import tools.markdown_resolve as mr

encoding = r'utf-8'
tf_python_dir = r'TensorFlow'
keras_dir = r'Keras'
pytorch_dir = r'PyTorch'

root_html_dir = r'tree_html'
root_md_dir = r'tree_md'

path_list = dict()
path_list[tf_python_dir] = []
path_list[keras_dir] = []
path_list[pytorch_dir] = []

crawler.crawl_tensor_flow_python_tree_structure(os.path.join(root_html_dir, tf_python_dir), path_list[tf_python_dir], encoding)
crawler.crawl_keras_tree_structure(os.path.join(root_html_dir, keras_dir), path_list[keras_dir], encoding)
crawler.crawl_pytorch_tree_structure(os.path.join(root_html_dir, pytorch_dir), path_list[pytorch_dir], encoding)

bh2m.batch_html_to_markdown_save_source(root_html_dir, root_md_dir, '.html', '.md', 0, encoding)

replace_reg = re.compile(r'.html$')
for index in path_list:
    for i in range(path_list[index].__len__()):
        path_list[index][i] = replace_reg.sub(r'.md', path_list[index][i][root_html_dir.__len__() + index.__len__() + 2:path_list[index][i].__len__()])
    open(os.path.join(root_md_dir, index, r'sidebar.json'), "w", encoding='utf-8').write(json.dumps(path_list[index]).replace('\\\\', '\\').replace('\\', '/'))

# open(r'single_backslash.json', "w", encoding='utf-8').write(json.dumps(path_list).replace('\\\\','\\'))


mr.batch_latex_to_embedded_html(root_md_dir)

for simple_dir in [keras_dir, pytorch_dir, tf_python_dir]:
    shutil.copy(r'generate_index.js', os.path.join(root_md_dir, simple_dir, r'generate_index.js'))
    cmd = r'cd "' + os.path.join(root_md_dir, simple_dir) + r'" && node generate_index.js'
    subprocess.call(cmd, shell=True)
    os.remove(os.path.join(root_md_dir, simple_dir, r'generate_index.js'))
    file_compress.make_targz(os.path.join(root_md_dir, simple_dir.lower() + r'.tar.gz'), os.path.join(root_md_dir, simple_dir))
