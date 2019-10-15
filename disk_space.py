# python3
####################################################################################################################################
# Program: disk_space.py
#  Author: Alessandro Carichini
#    Date: 12-08-2019
VERSION = '1.0819a'
####################################################################################################################################
# Moduli:
####################################################################################################################################
# http://www.unicode.org/ucd/
####################################################################################################################################

import sys
import os
import glob
import ntpath
import platform
import shutil
import time
import re
import argparse
import datetime

DEBUG = 0

OS_TARGA = platform.system()

UNICODE_FROM = "utf-8"
UNICODE_TO = ""

if OS_TARGA == "Windows":
    OS_TYPE = 1
else:
    OS_TYPE = 0

if OS_TYPE == 1:
    OS_SLASH = "\\"
else:
    OS_SLASH = "/"

PATH_OUT = os.getcwd()+ OS_SLASH

####################################################################################################################################
def remove_non_ascii(text):
    out = ''.join([i if ord(i) < 128 else ' ' for i in text])
    out2 = out.replace("\\n","\n")
    try:
        result = out2.encode('utf-8')
    except:
        result = "_UTF_8_"

    return result

def black_list_file(filename):
    myfilename = filename.upper().strip()
    if (myfilename in ['THUMBS.DB','THUMB.DB']):
        return True
    else:
        return False

def Get_Dir_Level(path):
    sep_dir = path.split(OS_SLASH)
    if OS_TYPE == 1:
        dec = 2
    else:
        dec = 1
    return len(sep_dir) - dec


def BytesToGB(n_bytes):
    return round(n_bytes / (1024*1024*1024),3)

def BytesToMB(n_bytes):
    return round(n_bytes / (1024*1024),3)


####################################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--dir', help='path_to_scan')
parser.add_argument('--read', help='file_db.sq3')
parser.add_argument('--level', help='dir depth level')
args = parser.parse_args()

if args.level is not None:
    n_level = int(args.level)
else:
    n_level = 1

if (args.dir <> ''):
    DirIN = args.dir
else:
    print("search_files_db --dir=path_to_scan --read=file_db.sq3")
    exit(1)

Start = time.time()
print("*** START ",time.strftime('%H:%M:%S'))

icount = 0
no_utf = 0

totbytes = 0
nLevel = 0

for root, directories, filenames in os.walk(DirIN):
    DIR_NAME = root
    nLevel = Get_Dir_Level(DIR_NAME)

    for filename in filenames:
        file = os.path.join(root, filename)
        filen1 = ntpath.basename(file)
        filen1_no_ext = os.path.splitext(filen1)[0]
        FILE_NAME = filen1

        if (not black_list_file(filen1)):
            FILE_DATA = File_Date_TS(file, 1)
            FILE_DT = FILE_DATA
            FILE_TS = 0

            fext = os.path.splitext(filen1)[1].upper()
            FILE_EXT = fext[1:].upper()

            FILE_PATH = os.path.dirname(file)

            try:
                FILE_SIZE = os.path.getsize(file)
            except:
                FILE_SIZE = -1

            totbytes = totbytes + FILE_SIZE

print("INSERTED: " + str(icount))
print("NO UTF  : "+str(no_utf))

print("**** END")
print(DiffTime(Start,time.time()))

print("Bytes")
print(totbytes)
