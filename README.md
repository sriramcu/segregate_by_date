# segregate_by_date
Recursively segregate files inside a directory by month and year.
This program extracts the actual recording date (instead of date modified in properties) of pictures and videos captured by a camera and moves them into directories according to month and year, while preserving the directory structure, which would consist of empty directories to remind the user of the original file classification. 

**Note to the user: As of now, there is no undo feature to put files back in their original folders. It is strongly advised to first make a copy elsewhere for backup.**

## Setup

Run the following commands on the terminal:  
`$ git clone https://github.com/sriramcu/segregate_by_date/`  
`$ cd segregate_by_date/`  
`$ pip install -r requirements.txt`

## Running the programs
Usage:  
`$ python3 segregator.py <directory_name>`  
`$ python3 merge.py <src_parent_directory> <dst_parent_directory>`

### 1. Segregate files into month and year (irreversible)

The following illustrates usage of this program with pictures captured on different dates, along with the [tree](https://linux.die.net/man/1/tree) command being executed before and after the program. These pictures are stored in different sub directories at different levels. assumptions.txt contains list of files whose date could not be determined accurately and were guessed from filename or file property, etc.
```console
(venv) sriram@sriram-e490:~/work/sample_pics$ tree
.
├── IMG_20190619_114041996.jpg
├── IMG_20190619_114042926.jpg
├── IMG_20190619_114046756.jpg
├── IMG_20190619_114047644.jpg
├── IMG_20190620_083506117.jpg
├── IMG_20190620_092138925.jpg
├── IMG_20190620_092528870_HDR.jpg
├── IMG_20190620_125941213_HDR.jpg
├── IMG_20190620_125947955_HDR.jpg
├── IMG_20190620_130007490_HDR.jpg
├── IMG_20190620_130009008_HDR.jpg
├── IMG_20190620_130024554_HDR.jpg
├── IMG_20190620_130033625_HDR.jpg
├── IMG_20190620_130037197_HDR.jpg
├── IMG_20190620_130039112_HDR.jpg
├── IMG_20190620_130053676_HDR.jpg
├── IMG_20190620_144406463.jpg
├── IMG_20190621_105340393_HDR.jpg
├── IMG_20190621_105341647_HDR.jpg
├── IMG_20190622_085150834_HDR.jpg
├── IMG_20190622_085153686_HDR.jpg
├── IMG_20190622_093343738_HDR.jpg
├── IMG_20190622_104219527.jpg
├── IMG_20190622_104220798.jpg
├── IMG_20190622_104222165.jpg
├── IMG_20190622_141249524_HDR.jpg
├── IMG_20190622_141250963_HDR.jpg
├── IMG_20190622_182856807.jpg
├── IMG_20190622_182857795.jpg
├── IMG_20190623_142047590.jpg
├── IMG_20190623_142048631.jpg
├── IMG_20190623_142051663.jpg
├── IMG_20190623_142053089.jpg
├── IMG_20190623_142652529.jpg
├── IMG_20190623_142653019.jpg
├── IMG_20190623_142734131.jpg
├── IMG_20190623_142734714.jpg
├── IMG_20190623_142737407.jpg
├── IMG_20190623_182416150.jpg
├── IMG_20190624_085719809.jpg
├── IMG_20190624_085720675.jpg
├── IMG_20190624_085721396.jpg
├── IMG_20190624_093332178.jpg
├── IMG_20190624_093332885.jpg
├── IMG_20190624_093351402.jpg
├── IMG_20190624_093353682.jpg
├── IMG_20190624_093617513.jpg
├── IMG_20190624_093619845.jpg
├── IMG_20190624_093621468.jpg
├── IMG_20190624_094610364.jpg
├── IMG_20190624_094611005.jpg
├── IMG_20190625_103641326.jpg
├── IMG_20190625_103642360.jpg
├── IMG_20190625_103645423.jpg
├── IMG_20190625_103647547.jpg
├── IMG_20190627_082155134.jpg
├── IMG_20190628_140531271.jpg
├── IMG_20190628_140533115.jpg
├── IMG_20190628_140534508.jpg
├── IMG_20190628_140539343.jpg
├── Screenshot_20190731-214549.png
├── VID_20190619_173815096.mp4
├── VID_20190619_181910931.mp4
├── VID_20190620_083417873.mp4
├── VID_20190620_083623680.mp4
├── VID_20190620_084845551.mp4
├── VID_20190620_091332045.mp4
├── VID_20190620_092131897.mp4
├── VID_20190620_130056499.mp4
├── VID_20190620_135050208.mp4
├── VID_20190622_104258541.mp4
├── VID_20190622_104736076.mp4
├── VID_20190622_141838742.mp4
├── VID_20190623_115313165.mp4
├── VID_20190624_093624100.mp4
└── VID_20190624_104007992.mp4

0 directories, 76 files
(venv) sriram@sriram-e490:~/work/sample_pics$ py ~/work/segregator.py .
1 out of 76 files have been segregated!
2 out of 76 files have been segregated!
3 out of 76 files have been segregated!
4 out of 76 files have been segregated!
5 out of 76 files have been segregated!
6 out of 76 files have been segregated!
7 out of 76 files have been segregated!
8 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190619_173815096.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190619_173815096.mp4 has been guessed as 2019
9 out of 76 files have been segregated!
10 out of 76 files have been segregated!
11 out of 76 files have been segregated!
12 out of 76 files have been segregated!
13 out of 76 files have been segregated!
14 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190623_115313165.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190623_115313165.mp4 has been guessed as 2019
15 out of 76 files have been segregated!
16 out of 76 files have been segregated!
17 out of 76 files have been segregated!
18 out of 76 files have been segregated!
19 out of 76 files have been segregated!
20 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_083417873.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_083417873.mp4 has been guessed as 2019
21 out of 76 files have been segregated!
22 out of 76 files have been segregated!
23 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_130056499.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_130056499.mp4 has been guessed as 2019
24 out of 76 files have been segregated!
25 out of 76 files have been segregated!
26 out of 76 files have been segregated!
27 out of 76 files have been segregated!
28 out of 76 files have been segregated!
29 out of 76 files have been segregated!
30 out of 76 files have been segregated!
31 out of 76 files have been segregated!
32 out of 76 files have been segregated!
33 out of 76 files have been segregated!
34 out of 76 files have been segregated!
35 out of 76 files have been segregated!
36 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_083623680.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_083623680.mp4 has been guessed as 2019
37 out of 76 files have been segregated!
38 out of 76 files have been segregated!
39 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_135050208.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_135050208.mp4 has been guessed as 2019
40 out of 76 files have been segregated!
41 out of 76 files have been segregated!
42 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190624_104007992.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190624_104007992.mp4 has been guessed as 2019
43 out of 76 files have been segregated!
44 out of 76 files have been segregated!
45 out of 76 files have been segregated!
46 out of 76 files have been segregated!
47 out of 76 files have been segregated!
48 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_084845551.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_084845551.mp4 has been guessed as 2019
49 out of 76 files have been segregated!
50 out of 76 files have been segregated!
51 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190622_141838742.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190622_141838742.mp4 has been guessed as 2019
52 out of 76 files have been segregated!
53 out of 76 files have been segregated!
54 out of 76 files have been segregated!
55 out of 76 files have been segregated!
56 out of 76 files have been segregated!
57 out of 76 files have been segregated!
/home/sriram/work/sample_pics/Screenshot_20190731-214549.png did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/Screenshot_20190731-214549.png has been guessed as 2019
58 out of 76 files have been segregated!
59 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190619_181910931.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190619_181910931.mp4 has been guessed as 2019
60 out of 76 files have been segregated!
61 out of 76 files have been segregated!
62 out of 76 files have been segregated!
63 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190622_104736076.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190622_104736076.mp4 has been guessed as 2019
64 out of 76 files have been segregated!
65 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190622_104258541.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190622_104258541.mp4 has been guessed as 2019
66 out of 76 files have been segregated!
67 out of 76 files have been segregated!
68 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190624_093624100.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190624_093624100.mp4 has been guessed as 2019
69 out of 76 files have been segregated!
70 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_091332045.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_091332045.mp4 has been guessed as 2019
71 out of 76 files have been segregated!
/home/sriram/work/sample_pics/VID_20190620_092131897.mp4 did not yield timestamp,guessing year...
Year for /home/sriram/work/sample_pics/VID_20190620_092131897.mp4 has been guessed as 2019
72 out of 76 files have been segregated!
73 out of 76 files have been segregated!
74 out of 76 files have been segregated!
75 out of 76 files have been segregated!
76 out of 76 files have been segregated!
(venv) sriram@sriram-e490:~/work/sample_pics$ cat assumptions.txt 
/home/sriram/work/sample_pics/VID_20190619_173815096.mp4
/home/sriram/work/sample_pics/VID_20190623_115313165.mp4
/home/sriram/work/sample_pics/VID_20190620_083417873.mp4
/home/sriram/work/sample_pics/VID_20190620_130056499.mp4
/home/sriram/work/sample_pics/VID_20190620_083623680.mp4
/home/sriram/work/sample_pics/VID_20190620_135050208.mp4
/home/sriram/work/sample_pics/VID_20190624_104007992.mp4
/home/sriram/work/sample_pics/VID_20190620_084845551.mp4
/home/sriram/work/sample_pics/VID_20190622_141838742.mp4
/home/sriram/work/sample_pics/Screenshot_20190731-214549.png
/home/sriram/work/sample_pics/VID_20190619_181910931.mp4
/home/sriram/work/sample_pics/VID_20190622_104736076.mp4
/home/sriram/work/sample_pics/VID_20190622_104258541.mp4
/home/sriram/work/sample_pics/VID_20190624_093624100.mp4
/home/sriram/work/sample_pics/VID_20190620_091332045.mp4
/home/sriram/work/sample_pics/VID_20190620_092131897.mp4
(venv) sriram@sriram-e490:~/work/sample_pics$ 
(venv) sriram@sriram-e490:~/work/sample_pics$ 
(venv) sriram@sriram-e490:~/work/sample_pics$ 
(venv) sriram@sriram-e490:~/work/sample_pics$ 
(venv) sriram@sriram-e490:~/work/sample_pics$ 
(venv) sriram@sriram-e490:~/work/sample_pics$ tree
.
├── 2019
│   ├── Jun
│   │   ├── IMG_20190619_114041996.jpg
│   │   ├── IMG_20190619_114042926.jpg
│   │   ├── IMG_20190619_114046756.jpg
│   │   ├── IMG_20190619_114047644.jpg
│   │   ├── IMG_20190620_083506117.jpg
│   │   ├── IMG_20190620_092138925.jpg
│   │   ├── IMG_20190620_092528870_HDR.jpg
│   │   ├── IMG_20190620_125941213_HDR.jpg
│   │   ├── IMG_20190620_125947955_HDR.jpg
│   │   ├── IMG_20190620_130007490_HDR.jpg
│   │   ├── IMG_20190620_130009008_HDR.jpg
│   │   ├── IMG_20190620_130024554_HDR.jpg
│   │   ├── IMG_20190620_130033625_HDR.jpg
│   │   ├── IMG_20190620_130037197_HDR.jpg
│   │   ├── IMG_20190620_130039112_HDR.jpg
│   │   ├── IMG_20190620_130053676_HDR.jpg
│   │   ├── IMG_20190620_144406463.jpg
│   │   ├── IMG_20190621_105340393_HDR.jpg
│   │   ├── IMG_20190621_105341647_HDR.jpg
│   │   ├── IMG_20190622_085150834_HDR.jpg
│   │   ├── IMG_20190622_085153686_HDR.jpg
│   │   ├── IMG_20190622_093343738_HDR.jpg
│   │   ├── IMG_20190622_104219527.jpg
│   │   ├── IMG_20190622_104220798.jpg
│   │   ├── IMG_20190622_104222165.jpg
│   │   ├── IMG_20190622_141249524_HDR.jpg
│   │   ├── IMG_20190622_141250963_HDR.jpg
│   │   ├── IMG_20190622_182856807.jpg
│   │   ├── IMG_20190622_182857795.jpg
│   │   ├── IMG_20190623_142047590.jpg
│   │   ├── IMG_20190623_142048631.jpg
│   │   ├── IMG_20190623_142051663.jpg
│   │   ├── IMG_20190623_142053089.jpg
│   │   ├── IMG_20190623_142652529.jpg
│   │   ├── IMG_20190623_142653019.jpg
│   │   ├── IMG_20190623_142734131.jpg
│   │   ├── IMG_20190623_142734714.jpg
│   │   ├── IMG_20190623_142737407.jpg
│   │   ├── IMG_20190623_182416150.jpg
│   │   ├── IMG_20190624_085719809.jpg
│   │   ├── IMG_20190624_085720675.jpg
│   │   ├── IMG_20190624_085721396.jpg
│   │   ├── IMG_20190624_093332178.jpg
│   │   ├── IMG_20190624_093332885.jpg
│   │   ├── IMG_20190624_093351402.jpg
│   │   ├── IMG_20190624_093353682.jpg
│   │   ├── IMG_20190624_093617513.jpg
│   │   ├── IMG_20190624_093619845.jpg
│   │   ├── IMG_20190624_093621468.jpg
│   │   ├── IMG_20190624_094610364.jpg
│   │   ├── IMG_20190624_094611005.jpg
│   │   ├── IMG_20190625_103641326.jpg
│   │   ├── IMG_20190625_103642360.jpg
│   │   ├── IMG_20190625_103645423.jpg
│   │   ├── IMG_20190625_103647547.jpg
│   │   ├── IMG_20190627_082155134.jpg
│   │   ├── IMG_20190628_140531271.jpg
│   │   ├── IMG_20190628_140533115.jpg
│   │   ├── IMG_20190628_140534508.jpg
│   │   └── IMG_20190628_140539343.jpg
│   ├── Screenshot_20190731-214549.png
│   ├── VID_20190619_173815096.mp4
│   ├── VID_20190619_181910931.mp4
│   ├── VID_20190620_083417873.mp4
│   ├── VID_20190620_083623680.mp4
│   ├── VID_20190620_084845551.mp4
│   ├── VID_20190620_091332045.mp4
│   ├── VID_20190620_092131897.mp4
│   ├── VID_20190620_130056499.mp4
│   ├── VID_20190620_135050208.mp4
│   ├── VID_20190622_104258541.mp4
│   ├── VID_20190622_104736076.mp4
│   ├── VID_20190622_141838742.mp4
│   ├── VID_20190623_115313165.mp4
│   ├── VID_20190624_093624100.mp4
│   └── VID_20190624_104007992.mp4
└── assumptions.txt

2 directories, 77 files
(venv) sriram@sriram-e490:~/work/sample_pics$ cat assumptions.txt 
/home/sriram/work/sample_pics/VID_20190619_173815096.mp4
/home/sriram/work/sample_pics/VID_20190623_115313165.mp4
/home/sriram/work/sample_pics/VID_20190620_083417873.mp4
/home/sriram/work/sample_pics/VID_20190620_130056499.mp4
/home/sriram/work/sample_pics/VID_20190620_083623680.mp4
/home/sriram/work/sample_pics/VID_20190620_135050208.mp4
/home/sriram/work/sample_pics/VID_20190624_104007992.mp4
/home/sriram/work/sample_pics/VID_20190620_084845551.mp4
/home/sriram/work/sample_pics/VID_20190622_141838742.mp4
/home/sriram/work/sample_pics/Screenshot_20190731-214549.png
/home/sriram/work/sample_pics/VID_20190619_181910931.mp4
/home/sriram/work/sample_pics/VID_20190622_104736076.mp4
/home/sriram/work/sample_pics/VID_20190622_104258541.mp4
/home/sriram/work/sample_pics/VID_20190624_093624100.mp4
/home/sriram/work/sample_pics/VID_20190620_091332045.mp4
/home/sriram/work/sample_pics/VID_20190620_092131897.mp4
(venv) sriram@sriram-e490:~/work/sample_pics$ 

```

### 2. Merge folders (irreversible)
This is used to combine the results of separate executions of segregator.py, for example merging files of 2018/May/ in different parent directories, etc.  





