import sys

sys.path.append('../..')
import tools.batch_html_to_markdown as bh2m
import os
import task.code_intelligence.crawl_data as crawler
import subprocess
import shutil
import tools.file_compress as file_compress
import tools.markdown_resolve as mr

encoding = r'utf-8'
tf_python_dir = r'TensorFlow'
keras_dir = r'Keras'
pytorch_dir = r'PyTorch'

root_html_dir = r'tree_html'
root_md_dir = r'tree_md'

crawler.crawl_tensor_flow_python_tree_structure(os.path.join(root_html_dir, tf_python_dir), encoding)
crawler.crawl_keras_tree_structure(os.path.join(root_html_dir, keras_dir), encoding)
crawler.crawl_pytorch_tree_structure(os.path.join(root_html_dir, pytorch_dir), encoding)

bh2m.batch_html_to_markdown_save_source(root_html_dir, root_md_dir, '.html', '.md', encoding)
mr.batch_remove_table_extra_line_break(root_md_dir, encoding)
mr.batch_latex_to_embedded_html(root_md_dir)

for dir in [keras_dir, pytorch_dir, tf_python_dir]:
    shutil.copy(r'generate_index.js', os.path.join(root_md_dir, dir, r'generate_index.js'))
    cmd = r'cd "' + os.path.join(root_md_dir, dir) + r'" && node generate_index.js'
    subprocess.call(cmd, shell=True)
    os.remove(os.path.join(root_md_dir, dir, r'generate_index.js'))
    file_compress.make_targz(os.path.join(root_md_dir, dir + r'.tar.gz'), os.path.join(root_md_dir, dir))
