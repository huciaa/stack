import os
from py7zr import unpack_7zarchive
import shutil


shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
dir_path = '/home/ec2-user'
files_zipped ='/home/ec2-user/files/'


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
    print(f)


