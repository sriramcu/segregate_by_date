import os
import sys
import magic
import re
from PIL import Image, ExifTags
import exiftool
import shutil
import datetime
from pathlib import Path
import platform
import calendar


class ExtractionException(Exception):
    pass


def move_file(src, dst):
    # Move without overwriting
    dst = os.path.abspath(dst)
    if os.path.dirname(src) == os.path.dirname(dst):
        # condition to ensure that file already present in the correct destination directory
        # does not get renamed as a duplicate in the next condition
        print("File already exists in the correct directory")
        return
    if os.path.exists(dst):
        dst_basename = "duplicate_" + os.path.basename(dst)
        dst_dirname = os.path.dirname(dst)
        while os.path.exists(os.path.join(dst_dirname, dst_basename)):
            dst_basename = "duplicate_" + dst_basename
        dst = os.path.join(dst_dirname, dst_basename)

    shutil.move(src, dst)


def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux.
            # No easy way to get creation dates here, so we'll settle for when its content was last modified.
            return stat.st_mtime


def is_video(fpath):
    mime = magic.Magic(mime=True)
    filename = mime.from_file(fpath)
    if filename.find('video') != -1:
        return 1
    return 0


def get_exif_date_time(fpath):
    try:
        if is_video(fpath):
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(fpath)
            dt = metadata['QuickTime:MediaCreateDate']

        else:
            img = Image.open(fpath)
            exif = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
            dt = exif['DateTimeOriginal']

        return (datetime.datetime.strptime(dt, "%Y:%m:%d %H:%M:%S").strftime("%b"),
                datetime.datetime.strptime(dt, "%Y:%m:%d %H:%M:%S").strftime("%Y"))

    except Exception as e:
        raise ExtractionException("Error in extracting date time from file: " + str(e))


def segregate_based_on_exif(fpath):
    try:
        (month, year) = get_exif_date_time(fpath)
        new_path = os.path.join('.', year, month)
        Path(new_path).mkdir(parents=True, exist_ok=True)
        move_file(fpath, os.path.join(new_path, os.path.basename(fpath)))

    except ExtractionException:
        # pass/send exception to caller
        raise ExtractionException


def segregate_based_on_file_name(fpath):
    current_year = datetime.datetime.now().year
    years = list(range(1980, current_year))  # function guesses year if year 1980 to 2021 is present in file name
    basename = str(os.path.basename(fpath))
    dirname = str(os.path.dirname(fpath))

    for year in years:
        if str(year) in dirname:
            # Already Segregated
            return 1

        if str(year) in basename:
            date_regex = re.compile(str(year) + r'[-_]?(\d{1,2})')
            # Year and month may be separated by hyphen or underscore
            mo = date_regex.search(basename)
            if not mo or int(mo.group(1)) > 12:
                exif_flag = 0
                try:
                    exif_month, exif_year = get_exif_date_time(fpath)
                except ExtractionException:
                    exif_month = None
                    exif_year = None
                    exif_flag = 1

                if not exif_flag and int(exif_year) == year:
                    month = exif_month
                    print("Year and Month for {} have been guessed as {}-{}".format(fpath, year, month))
                    new_path = os.path.join('.', str(year), month)
                    Path(new_path).mkdir(parents=True, exist_ok=True)
                    move_file(fpath, os.path.join(new_path, basename))
                    return 1

                print("Year for {} has been guessed as {}".format(fpath, year))
                new_path = os.path.join('.', str(year))
                Path(new_path).mkdir(parents=True, exist_ok=True)
                move_file(fpath, os.path.join(new_path, basename))
                return 1

            else:
                month = str(mo.group(1))
                month = calendar.month_abbr[int(month)]
                print("Year and Month for {} have been guessed as {}-{}".format(fpath, year, month))
                new_path = os.path.join('.', str(year), month)
                Path(new_path).mkdir(parents=True, exist_ok=True)
                move_file(fpath, os.path.join(new_path, basename))
                return 1

    return 0


def segregate_based_on_creation_date(fpath):
    try:
        year = datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%Y')
        month = datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%b')
    except Exception:
        raise ExtractionException
        # return 0
    print("Year and month for {} have been guessed as {},{}".format(fpath, year, month))
    new_path = os.path.join('.', year, month)
    Path(new_path).mkdir(parents=True, exist_ok=True)
    move_file(fpath, os.path.join(new_path, os.path.basename(fpath)))
    return 1


def main():
    os.chdir(sys.argv[1])
    # Argument must specify parent directory containing the files to be segregated; this program preserves all directories
    assumptions_file_name = "assumptions.txt"
    assumptions_file_pointer = open(assumptions_file_name, 'w')  # Stores names of files whose date were guessed

    l = sum([len(files) for r, d, files in os.walk(".")]) - 1
    i = 0
    files_list = []
    for (root, dirs, files) in os.walk('.', topdown=True):
        for img_file_path in files:
            files_list.append(os.path.abspath(os.path.join(root, img_file_path)))

    for img_file_path in files_list:
        if i:
            print("{} out of {} files have been segregated!".format(i, l))
        i += 1
        if assumptions_file_name in img_file_path:
            continue

        flag = segregate_based_on_file_name(img_file_path)
        if flag:
            continue

        try:
            segregate_based_on_exif(img_file_path)
        except ExtractionException:
            print("Not able to get actual timestamp of {}, segregating based on creation date...".format(img_file_path))
            assumptions_file_pointer.write(img_file_path + '\n')
            try:
                segregate_based_on_creation_date(img_file_path)
            except ExtractionException:
                print("Year for {} could not be guessed".format(img_file_path))
                move_file(img_file_path, os.path.join(os.path.abspath(sys.argv[1]), os.path.basename(img_file_path)))

    print("{} out of {} files have been segregated!".format(i, l))
    assumptions_file_pointer.close()


if __name__ == '__main__':
    # todo merge program and GUI
    main()
