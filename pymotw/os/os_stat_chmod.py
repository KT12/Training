import os
import stat

# File permissions can be changed by chmod()
# https://pymotw.com/3/os/

def main():
    filename = 'os_stat_chmod_example.txt'
    if os.path.exists(filename):
        os.unlink(filename) # os.unlink(file) deletes file
    with open(filename, 'wt') as f:
        f.write('contents')

    # Determine what permissions are set using stat
    existing_permissions = stat.S_IMODE(os.stat(filename).st_mode)

    if not os.access(filename, os.X_OK):
        print('Adding execute permission')
        new_permissions = existing_permissions | stat.S_IXUSR
    else:
        print('Removing execute permission')
        # use XOR to remove the user execute permission
        new_permissions = existing_permissions ^ stat.S_IXUSR
    
    os.chmod(filenam, new_permissions)

if __name__ == '__main__':
    main()