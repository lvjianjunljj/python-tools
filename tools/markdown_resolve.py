import os
import subprocess


def batch_latex_to_embedded_html(input_root_dir, system_name):
    list_dirs = os.walk(input_root_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            input_file_full_path = os.path.join(root, f)
            cmd = r'node generate_latex.js -i "' + input_file_full_path + r'" -o "' + input_file_full_path
            if system_name =='windows_cmd':
                cmd += r'">nul'
            elif system_name == 'windows_powershell':
                cmd += r'">$null'
            elif system_name == 'linux':
                cmd += r'"/dev/null'
            else:
                cmd += r'"'
            subprocess.call(cmd, shell=True)
