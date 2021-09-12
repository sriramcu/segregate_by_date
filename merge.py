import os
import shutil
import sys


def move_file(src, dst):
    # Move without overwriting
    # Hello World
    dst = os.path.abspath(dst)
    if os.path.exists(dst):
        dst_basename = "duplicate_" + os.path.basename(dst)
        dst_dirname = os.path.dirname(dst)
        while os.path.exists(os.path.join(dst_dirname, dst_basename)):
            dst_basename = "duplicate_" + dst_basename
        dst = os.path.join(dst_dirname, dst_basename)

    shutil.move(src, dst)


def main():
    parent_dir = os.path.abspath(sys.argv[1])
    os.chdir(parent_dir)
    dst_parent_dir = os.path.abspath(sys.argv[2])


if __name__ == '__main__':
    main()
