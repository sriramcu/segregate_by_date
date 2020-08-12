import os
import sys
import magic
from PIL import Image, ExifTags
import exiftool
import shutil
import datetime 
from pathlib import Path

class ExtractionException(Exception):
    pass

import platform

def creation_date(path_to_file):
    
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here, so we'll settle for when its content was last modified.
            return stat.st_mtime
            
def isVideo(fpath):
    mime = magic.Magic(mime=True)
    filename = mime.from_file(fpath)
    if filename.find('video') != -1:
       return 1
    return 0

def getDateTime(fpath):
    try:
        if isVideo(fpath):
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata('VID_20190319_200906.mp4')
            dt = metadata['QuickTime:MediaCreateDate']
            

        img = Image.open(f)
        
        exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
       
        dt = exif['DateTimeOriginal']
        
       
        return (datetime.datetime.strptime(dt,"%Y:%m:%d %H:%M:%S").strftime("%b"), datetime.datetime.strptime(dt,"%Y:%m:%d %H:%M:%S").strftime("%Y"))
        
    except Exception:
        raise ExtractionException
    



    
def segregate(fpath):
    try:
        (month,year) = getDateTime(fpath)
        newpath = os.path.join('.',year,month)
        Path(newpath).mkdir(parents=True, exist_ok=True)
        shutil.move(fpath,os.path.join(newpath,os.path.basename(fpath)))

    except ExtractionException:
        raise ExtractionException
    
def uncertain_segregate(fpath):
    years = list(range(1980,2021)) #function guesses year if year 1980 to 2020 is present in file name
    
    for year in years:
        if str(os.path.basename(fpath)).startswith(str(year)) or str(os.path.basename(fpath)).startswith("IMG-"+str(year)):
            print("Year for {} has been guessed as {}".format(fpath,year))
            newpath = os.path.join('.',str(year))
            Path(newpath).mkdir(parents=True, exist_ok=True)
            shutil.move(fpath,os.path.join(newpath,os.path.basename(fpath)))
            return 1
            
            
    for year in years:
        if str(year) in str(fpath): #if above criteria fails; basename not taken here so that it considers years for manually segregated files
            print("Year for {} has been guessed as {}".format(fpath,year))
            newpath = os.path.join('.',str(year))
            Path(newpath).mkdir(parents=True, exist_ok=True)
            shutil.move(fpath,os.path.join(newpath,os.path.basename(fpath)))
            return 1
    
    try:    
        year = datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%Y')
        month =  datetime.datetime.fromtimestamp(creation_date(fpath)).strftime('%b')
    except Exception:
        raise ExtractionException
        return 0
    print("Year and month for {} have been guessed as {},{}".format(fpath,year,month))
    newpath = os.path.join('.',year,month)
    Path(newpath).mkdir(parents=True, exist_ok=True)
    shutil.move(fpath,os.path.join(newpath,os.path.basename(fpath)))
    return 1
    
    
            
if __name__ == '__main__':
    os.chdir(sys.argv[1]) #Argument must specify parent directory containing the files to be segregated; this program preserves all directories 
    f1 = open("assumptions.txt",'w') #Stores names of files whose date were guessed
    
    
    l = sum([len(files) for r, d, files in os.walk(".")]) - 1
    i=1
    files_list = []
    for (root,dirs,files) in os.walk('.', topdown=True):
        for f in files:
            files_list.append(os.path.abspath(os.path.join(root,f)))
            
    
    for f in files_list:
        if "assumptions.txt" in f:
            continue
        try:
            segregate(f)
        except ExtractionException:
            print("{} did not yield timestamp,guessing year...".format(f))
            f1.write(f+'\n')
            try:
                flag = uncertain_segregate(f)
            except ExtractionException: 
                print("Year for {} could not be guessed".format(f))
                #shutil.move(f,os.path.join(os.path.abspath(sys.argv[1]),os.path.basename(f)))
            
        print("{} out of {} files have been segregated!".format(i,l))
        i+=1
        
    f1.close()
