# coding=utf-8
import requests
import datetime
from bs4 import BeautifulSoup
import csv
import wget
import pandas as pd
import os
import glob
from math import ceil
from py7zr import unpack_7zarchive
import shutil
import subprocess

shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
dir_path = '/home/ec2-user'
files_zipped ='/home/ec2-user/files/'
files_unpacked = '/home/ec2-user/unpack'


def unpack():
    files = [f for f in os.listdir(files_zipped) if os.path.isfile(files_zipped+f)]
    for f in files:
        if ".7z" in f and ".meta." in f and ".tmp" not in f and "stackoverflow" not in f:
            directory = dir_path+'/unpack/'+f.split('.')[0]+'.meta/'

        elif ".7z" in f and ".tmp" not in f and "stackoverflow" not in f:
            directory = dir_path+'/unpack/'+f.split('.')[0]+'/'
        else:
            continue
        if not os.path.exists(directory):
            os.makedirs(directory)
        #Archive(dir_path + '/' + f).extractall(directory)
        shutil.unpack_archive(files_zipped + '/' + f, directory)
        print(f+" saved")
        os.remove(os.path.join(files_zipped, f))

def run_splitter():
    files = [f for f in glob.iglob(files_unpacked + '**/**', recursive=True)]
    for f in files:
            if os.path.isfile(f):
                    size =os.stat(f).st_size/(1024*1024)
                    if int(size) > 100:
                            split(f)
                            print("THE FILE "+f+" HAS BEEN SPLITTED")
def split(file):
    with open(file, 'r') as f:
        data = f.readlines()
    line = 2
    batch = 1
    max = 10000
    batches = ceil(len(data) / 10000)
    openLine = '<?xml version="1.0" encoding="utf-8"?>\n'
    openTag = data[1]
    closeTag = data[-1]

    for a in range(batch, batches + 1, 1):
        filename= file.replace('.xml', str(a)+'.xml')
        with open(filename, 'a+') as f:
            f.write(openLine)
            f.write(openTag)
            while line <= a * max and line < len(data) - 1:
                f.write(data[line])
                line += 1
            f.write(closeTag)
    os.remove(file)


# POBIERANIE DANYCH ZE STRONY
r = requests.get('https://archive.org/download/stackexchange')
soup = BeautifulSoup(r.text, 'html.parser')
populate_files_downloaded = 0

# WCZYTYWANIE DANYCH ZE STRONY DO LISTY
files = []
for tr in soup.find_all('tr')[1:]:
    tds = tr.find_all('td')
    if '7z' in tds[0].text:
        files.append([tds[0].text[:-16], tds[1].text])

# WCZYTYWANIE OBECNIE POBRANYCH WERSJI PLIKÓW DO PORÓWNANIA
with open('files_downloaded.txt', newline='') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    files_downloaded = pd.DataFrame(list(reader))

files_to_download = pd.DataFrame(files)

# TEN FRAGMENT KODU POZWALA STWORZYĆ PLIK FILES_DOWNLOADED.TXT KTÓRY BĘDZIE PÓŹNIEJ POTRZEBNY DO TRZYMANIA WERSJI PLIKU
if populate_files_downloaded:
    files_to_download[1] = '01-Jan-2010 00:00'
    filelist = files_to_download.values.tolist()
    file = open('files_downloaded.txt', 'w+', newline='')
    with file:
        write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        write.writerows(filelist)
    exit()

for index, row in files_to_download.iterrows():
    date_from_server = datetime.datetime.strptime(row[1], '%d-%b-%Y %H:%M')
    date_from_file = datetime.datetime.strptime(
        files_downloaded[1][files_downloaded[0] == row[0]].to_string(index=False),
        '%d-%b-%Y %H:%M')
    if date_from_server > date_from_file:
        print("There is a newer version of {file}, starting download".format(file=row[0]))
        wget.download("https://archive.org/download/stackexchange/" + row[0], out='/home/ec2-user/files')
        files_downloaded[1][files_downloaded[0] == row[0]] = row[1]
        file = open('files_downloaded.txt', 'w+', newline='')
        with file:
            write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            write.writerows(files_downloaded.values.tolist())
        print('{file} saved'.format(file=row[0]))
    unpack()
    run_splitter()
    subprocess.call("/home/ec2-user/stack/import.sh")








