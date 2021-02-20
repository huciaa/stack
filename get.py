import requests
import datetime
from bs4 import BeautifulSoup
import csv
import wget
import pandas as pd


# POBIERANIE DANYCH ZE STRONY
r = requests.get('https://archive.org/download/stackexchange')
soup = BeautifulSoup(r.text, 'html.parser')

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
# for a in files:
#     date_time_str = a[1]
#     date_time_obj = datetime.datetime.strptime(date_time_str, '%d-%b-%Y %H:%M')
#     print('Date:', date_time_obj.date())
#     print('Time:', date_time_obj.time())
#     print('Date-time:', date_time_obj)
#     print(a[1])

# TEN FRAGMENT KODU POZWALA STWORZYĆ PLIK FILES_DOWNLOADED.TXT KTÓRY BĘDZIE PÓŹNIEJ POTRZEBNY DO TRZYMANIA WERSJI PLIKU
# files_to_download[1] = '01-Jan-2010 00:00'
# filelist = files_to_download.values.tolist()
# file = open('files_downloaded.txt', 'w+', newline='')
# with file:
#     write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#     write.writerows(filelist)

# wget.download("https://archive.org/download/stackexchange/"+"writers.meta.stackexchange.com.7z")
# print(files_to_download[files_to_download[0]=='writers.meta.stackexchange.com.7z'])
#files[0].index(files[34][0])

# for a in files_to_download.iterrows():
    # print("File name: {file}, file version on server: {date}, file version downloaded: {currentDate}".format(file = a[1], date = a[2],currentDate = 'lel'))
    # print(a[1])

# for index, row in files_to_download.iterrows():
#     print("""File name: {file},
#      file version on server: {date},
#       file version downloaded: {currentDate}""".format(
#         file=row[0], date=row[1], currentDate=files_downloaded[1][files_downloaded[0] == row[0]]))

for index, row in files_to_download.iterrows():
    date_from_server = datetime.datetime.strptime(row[1], '%d-%b-%Y %H:%M')
    date_from_file = datetime.datetime.strptime(
        files_downloaded[1][files_downloaded[0] == row[0]].to_string(index=False),
        '%d-%b-%Y %H:%M')
    if date_from_server > date_from_file:
        print("There is a newer version of {file}, starting download".format(file=row[0]))
        wget.download("https://archive.org/download/stackexchange/" + row[0])
        files_downloaded[1][files_downloaded[0] == row[0]] = row[1]
        file = open('files_downloaded.txt', 'w+', newline='')
        with file:
            write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            write.writerows(files_downloaded.values.tolist())
        print('{file} saved'.format(file=row[0]))
