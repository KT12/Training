import os
import sys

# Function traverses a directory recursively
# https://pymotw.com/3/os/

# Run from interpreter as follows to check directory up one level
# >>> python3 os_walk.py '../'

def main():
    if len(sys.argv) == 1:
        root = '/home/ktt/Training'
    else:
        # Don't use '~' as root, will take LONG time to run
        root = sys.argv[1]
    
    for dir_name, sub_dirs, files in os.walk(root):
        print(dir_name)
        # Make subd names stand out with '/'
        sub_dirs = [n + '/' for n in sub_dirs]
        # Mix directory contents together
        contents = sub_dirs + files
        contents.sort()
        # Show contents
        for c in contents:
            print('    {}'.format(c))
        print()

if __name__ == '__main__':
    main()