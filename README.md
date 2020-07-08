# segregate_by_date
Recursively segregate files inside a directory by month and year.
This program extracts the actual recording date of pictures and videos captured by a camera and moves them into directories according to month and year, while preserving the directory structure, which would consist of empty directories to remind the user of the original file classification. 

**Note to the user: As of now, there is no undo feature to put back files in their original folders. It is strongly advised to first make a copy elsewhere for backup**

## Prerequisites
The following modules need to be installed, by calling the 
` pip install <module_name> command`
* magic (module_name in above command for this would be 'python-magic')
* PIL
* exiftool
* pathlib
* datetime

## Installation

Run the following command on the terminal:  
`$ git clone https://github.com/sriramcu/segregate_by_date/`

## Running the program
Usage:  
`$ python3 segregator.py <directory_name>`  

## Examples

### 1. Segregate files into month and year(irreversible)

The following illustrates usage of this program with pictures captured on different dates, along with the [tree](https://linux.die.net/man/1/tree) command being executed before and after the program. These pictures are stored in different sub directories at different levels.  


### 2. Recursively move all files inside subdirectory tree (irreversible)  

This is similar to shutil.copytree, however it preserves the directory structure, which would consist of empty directories to remind the user of the original file classification. The following illustrates usage of the program movetree.py with  the [tree](https://linux.die.net/man/1/tree) command being executed before and after the program. These files are stored in different sub directories at different levels.   
We may use this program if it is necessary for all files to be at the same directory level; such as showing pictures on a TV by pressing next button on the remote without having to navigate to another directory.
