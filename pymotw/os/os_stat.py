import os
import sys
import time

# Use lstat() or stat() for detailed info
# https://pymotw.com/3/os/

def main():
    if len(sys.argv) == 1:
        filename = __file__
    else:
        filename = sys.argv[1]
    
    stat_info = os.stat(filename)
    print('os.stat({}):'.format(filename))
    print('     Size:', stat_info.st_size)
    print('     Permissions:', oct(stat_info.st_mode))
    print('     Owner:', stat_info.st_uid)
    print('     Device:', stat_info.st_dev)
    print('     Created      :', time.ctime(stat_info.st_ctime))
    print('     Last modified:', time.ctime(stat_info.st_mtime))
    print('     Last accessed:', time.ctime(stat_info.st_atime))

if __name__ == '__main__':
    main()