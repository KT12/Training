import os
import sys

# `scandir()` collects info in one system call
# https://pymotw.com/3/os/

# Run from interpreter as follows to check current directory:
# >>> python3 os_scandir.py .

def main():
    for entry in os.scandir(sys.argv[1]):
        if entry.is_dir():
            typ = 'dir'
        elif entry.is_file():
            typ = 'file'
        elif entry.is_symlink():
            typ = 'link'
        else:
            typ = 'unknown'
        print('{name}\t{typ}'.format(name=entry.name, typ=typ,))

if __name__ == '__main__':
    main()