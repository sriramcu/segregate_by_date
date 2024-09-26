import argparse
import calendar
import datetime
import mimetypes
import os
import platform
import re
import shutil
from pathlib import Path, PurePath

import exiftool
from PIL import Image, ExifTags

VERBOSE = False
ASSUMPTIONS_FILE_NAME = "assumptions.txt"
TIMESTAMP_STR = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class ExtractionException(Exception):
    pass


def segregate_based_on_creation_date(fpath, output_dir):
    try:
        year = datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%Y')
        month = datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%b')
    except Exception:
        return False
    else:
        print_and_log(f"Year and month for {fpath} have been guessed as {year}, {month}", output_dir)
        new_path = os.path.join(output_dir, year, month)
        Path(new_path).mkdir(parents=True, exist_ok=True)
        shutil.move(fpath, os.path.join(new_path, os.path.basename(fpath)))
        return True


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
    mt = mimetypes.guess_type(fpath)
    if not mt:
        return 0
    if "video" in mt[0]:
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


def segregate_based_on_exif(fpath, output_dir):
    try:
        (month, year) = get_exif_date_time(fpath)
        new_path = os.path.join(output_dir, year, month)
        Path(new_path).mkdir(parents=True, exist_ok=True)
        shutil.move(fpath, os.path.join(new_path, os.path.basename(fpath)))
        return True
    except ExtractionException:
        return False


def segregate_based_on_file_name(fpath, output_dir):
    basename = str(os.path.basename(fpath))
    dirname = str(os.path.dirname(fpath))

    current_year = datetime.datetime.now().year
    years = list(range(1980, current_year))

    for year in years:
        if str(year) in PurePath(dirname).parts:
            # Already Segregated
            return True

        if str(year) in basename:
            date_regex = re.compile(str(year) + r'[-_]?(\d{1,2})')
            # Year and month may be separated by hyphen or underscore
            mo = date_regex.search(basename)
            if not mo or int(mo.group(1)) > 12 or int(mo.group(1)) < 1:
                # Month not found in the basename of the file. Now try using EXIF metadata,
                # since we already have year in the file name. In segregate by exif function, we only look at exif
                # metadata without any regard to file or folder name.
                exif_flag = False
                try:
                    exif_month, exif_year = get_exif_date_time(fpath)
                    # even though we have the year already, we are still going to validate the exif year with the filename
                    # year. If the exif year is not equal to the filename year then we are not going to move the file
                except ExtractionException:
                    exif_month = None
                    exif_year = None
                    exif_flag = True

                if not exif_flag and int(exif_year) == year:
                    # No extraction error and exif year and filename year are same. Proceed to use exif month too.
                    month = exif_month
                    print_and_log(f"Year and Month for {fpath} have been guessed as {year}-{month}",
                                  output_dir)
                    new_path = os.path.join(output_dir, str(year), month)
                    Path(new_path).mkdir(parents=True, exist_ok=True)
                    shutil.move(fpath, os.path.join(new_path, basename))
                    return True

                print_and_log(f"Year for {fpath} has been guessed as {year}", output_dir)
                new_path = os.path.join(output_dir, str(year))
                Path(new_path).mkdir(parents=True, exist_ok=True)
                shutil.move(fpath, os.path.join(new_path, basename))
                return True

            else:
                # No need for exif. Use year and month embedded in filename
                month = str(mo.group(1))
                month = calendar.month_abbr[int(month)]
                print_and_log(f"Year and Month for {fpath} have been guessed as {year}-{month}", output_dir)
                new_path = os.path.join(output_dir, str(year), month)
                Path(new_path).mkdir(parents=True, exist_ok=True)
                shutil.move(fpath, os.path.join(new_path, basename))
                return True

    return False


def print_and_log(msg, output_dir, first_time=False, verbose=VERBOSE):
    if first_time:
        mode = 'w'
    else:
        mode = 'a'
    if verbose:
        print(msg)

    assumptions_file_path = os.path.join(output_dir, ASSUMPTIONS_FILE_NAME)
    assumptions_file_pointer = open(assumptions_file_path, mode)  # Stores names of files whose date were guessed
    assumptions_file_pointer.write(msg + '\n')
    assumptions_file_pointer.close()


def get_directory_stats(path):
    total_size = 0
    file_count = 0
    if os.path.exists(path):
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                # Skip if it's a broken symlink
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
                    file_count += 1

    return file_count, total_size


def backup_input_or_output_folder(directory, output_dir):
    """
    Creates a backup of the input or output folder.The backup folder will be a sibling to directory and the actual
    backup is stored inside the appropriate timestamp folder.
    :param directory:
    :return:
    """
    print_and_log(f"Backing up {directory}", output_dir)

    backup_dir = os.path.join(os.path.dirname(directory), 'program_backup', TIMESTAMP_STR, os.path.basename(directory))
    os.makedirs(backup_dir, exist_ok=True)
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            os.makedirs(os.path.join(backup_dir, os.path.relpath(directory_path, directory)), exist_ok=True)
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(backup_dir, os.path.relpath(root, directory), file))

    print_and_log(f"Backup of {directory} completed", output_dir)
    # cleanup old backups
    backup_parent_dir = os.path.join(os.path.dirname(directory), 'program_backup')
    if not os.path.exists(backup_parent_dir):
        return
    backups = [os.path.join(backup_parent_dir, f) for f in sorted(os.listdir(backup_parent_dir), reverse=True)]
    for backup in backups[4:]:
        shutil.rmtree(backup)


def segregate_entire_folder(input_dir, output_dir):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory {input_dir} does not exist")
    os.makedirs(output_dir, exist_ok=True)
    print_and_log(f"File count and file size of input folder {input_dir} is {get_directory_stats(input_dir)}",
                  output_dir, verbose=True, first_time=True)
    print_and_log(f"Before program run, file count and file size of output folder {output_dir}"
                  f" is {get_directory_stats(output_dir)}", output_dir, verbose=True)
    backup_input_or_output_folder(input_dir, output_dir)
    if (get_directory_stats(output_dir)[0] > 1):
        backup_input_or_output_folder(output_dir, output_dir)
    for (root, dirs, files) in os.walk(input_dir, topdown=True):
        for img_file_name in files:
            if ASSUMPTIONS_FILE_NAME in img_file_name:
                continue
            img_file_path = os.path.abspath(os.path.join(root, img_file_name))

            status_flag = segregate_based_on_file_name(img_file_path, output_dir)
            if status_flag:
                continue
            print_and_log(f"Unable to segregate {img_file_path} based on its file name.", output_dir)

            status_flag = segregate_based_on_exif(img_file_path, output_dir)
            if status_flag:
                continue
            print_and_log(f"Unable to segregate {img_file_path} based on its EXIF metadata.", output_dir)

            status_flag = segregate_based_on_creation_date(img_file_path, output_dir)
            if status_flag:
                continue
            print_and_log(f"Unable to segregate {img_file_path} based on its creation date.", output_dir)

            unknown_dir_path = os.path.join(os.path.abspath(output_dir), "Unknown")
            os.makedirs(unknown_dir_path, exist_ok=True)
            shutil.move(img_file_path, os.path.join(unknown_dir_path, img_file_name))

    print_and_log(f"After program run, file count and file size of output folder {output_dir}"
                  f" is {get_directory_stats(output_dir)}", output_dir, verbose=True)
    if len(os.listdir(input_dir)) == 0:
        shutil.rmtree(input_dir)


def main():
    parser = argparse.ArgumentParser(description='Segregate files into folders based on their date')
    parser.add_argument('-d', '--input_dir', type=str, required=True,
                        help='Absolute path of folder containing the files to be segregated')
    parser.add_argument('-o', '--output_dir', type=str, required=True,
                        help='Absolute path of output directory')
    parser.add_argument('-v', '--verbose', type=int, default=0,
                        help='Print status messages as the program runs')
    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    global VERBOSE
    VERBOSE = bool(int(args.verbose))
    segregate_entire_folder(input_dir, output_dir)


if __name__ == '__main__':
    main()
