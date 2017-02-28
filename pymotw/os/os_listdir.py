import os
import sys

# Prepares a list of the contents of the directory
# https://pymotw.com/3/os/

# Run from CLI
# >>> python3 os_listdir.py .

def main():
    print(os.listdir(sys.argv[1]))

if __name__ == "__main__":
    main()