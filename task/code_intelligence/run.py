import tools.batch_html_to_markdown as bh2m
import os
import task.code_intelligence.crawl_data as crawler
import subprocess
import shutil
import tools.file_compress as file_compress

tf_python_dir = r'tensorflow'
keras_dir = r'keras'
pytorch_dir = r'pytorch'

root_html_dir = r'.\tree html'
root_md_dir = r'.\tree md'

crawler.crawl_tensor_flow_python_tree_structure(os.path.join(root_html_dir, tf_python_dir), 'gb18030')
crawler.crawl_keras_tree_structure(os.path.join(root_html_dir, keras_dir), 'gb18030')
crawler.crawl_pytorch_tree_structure(os.path.join(root_html_dir, pytorch_dir), 'gb18030')

bh2m.batch_html_to_markdown_save_source(root_html_dir, root_md_dir, '.html', '.md', 'gb18030')

for dir in [keras_dir, pytorch_dir, tf_python_dir]:
    shutil.copy(r'.\dist.js', os.path.join(root_md_dir, dir, r'dist.js'))
    cmd = r'cd "' + os.path.join(root_md_dir, dir) + r'" && node dist.js'
    subprocess.call(cmd, shell=True)
    os.remove(os.path.join(root_md_dir, dir, r'dist.js'))
    file_compress.make_targz(os.path.join(root_md_dir, dir + r'.tar.gz'), os.path.join(root_md_dir, dir))
