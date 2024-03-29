import os
import shutil
import sys
import datetime
import calendar
import filecmp
from pathlib import Path


current_year = datetime.datetime.now().year
years = list(range(1980, current_year))


def copy_file(src, dst):
    # Move without overwriting
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    if os.path.exists(dst):
        if filecmp.cmp(src, dst, shallow=False):
            return
        dst_basename = "duplicate_" + os.path.basename(dst)
        dst_dirname = os.path.dirname(dst)
        while os.path.exists(os.path.join(dst_dirname, dst_basename)):
            dst_basename = "duplicate_" + dst_basename
        dst = os.path.join(dst_dirname, dst_basename)

    shutil.copy(src, dst)


def main():
    # copy src to dst and merge in dst
    if len(sys.argv) < 3:
        print("Usage: python3 merge.py src_dir dst_dir")
        sys.exit(-1)

    src_parent_dir = os.path.abspath(sys.argv[1])
    dst_parent_dir = os.path.abspath(sys.argv[2])

    os.chdir(src_parent_dir)

    src_files_list = []
    for (root, dirs, files) in os.walk('.', topdown=True):
        for img_file_path in files:
            src_files_list.append(os.path.abspath(os.path.join(root, img_file_path)))

    os.chdir(dst_parent_dir)

    for src_file in src_files_list:
        components = os.path.normpath(src_file).split(os.path.sep)
        if "assumptions" in src_file:
            continue
        selected_year = None
        selected_month = None
        for year in years:
            if str(year) in components:
                selected_year = str(year)

        for month in calendar.month_abbr:
            if month in components and month.strip() != '':
                selected_month = month

        if not selected_year:
            raise Exception("Source parent directory is not segregated. Run the segregator program before merging")
        elif not selected_month:
            new_path = os.path.join('.', selected_year)
        else:
            new_path = os.path.join('.', selected_year, selected_month)

        Path(new_path).mkdir(parents=True, exist_ok=True)
        copy_file(src_file, os.path.join(new_path, os.path.basename(src_file)))


if __name__ == '__main__':
    main()
