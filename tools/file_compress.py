import os
import tarfile
import zipfile


# Package directory as zip file (uncompressed)
def make_zip(output_file,source_dir):
    zipf = zipfile.ZipFile(output_file, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()




# Package the entire root directory at once. Empty subdirectories will be packaged.
# If the package is not compressed, change the "w:gz" parameter to "w:" or "w".
def make_targz(output_file, source_dir):
    #replace the exist gz file
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


# Add files one by one, and empty subdirectories are not packaged. Filter files.
# If the package is not compressed, change the "w:gz" parameter to "w:" or "w".
def make_targz_one_by_one(output_file, source_dir):
    tar = tarfile.open(output_file, "w:gz")
    for root, dir, files in os.walk(source_dir):
        for file in files:
            pathfile = os.path.join(root, file)
            tar.add(pathfile)
    tar.close()