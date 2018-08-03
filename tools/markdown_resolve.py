import os
import subprocess
import platform


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
                cmd += r'"/dev/null'
            else:
                # other system
                cmd += r'"'
            subprocess.call(cmd, shell=True)
