import os


# Traverse directory
def method1(root_dir):
    list_dirs = os.walk(root_dir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print(os.path.join(root, d))
        for f in files:
            print(os.path.join(root, f))


def method2(root_dir):
    for lists in os.listdir(root_dir):
        path = os.path.join(root_dir, lists)
        print(path)
        if os.path.isdir(path):
            method2(path)