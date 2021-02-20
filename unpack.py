import os
from pyunpack import Archive

dir_path = os.path.dirname(os.path.realpath(__file__))
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if ".7z" in f and ".meta." in f and ".tmp" not in f and "stackoverflow" not in f:
        directory = dir_path+'\\'+f.split('.')[0]+'.meta\\'

    elif ".7z" in f and ".tmp" not in f and "stackoverflow" not in f:
        directory = dir_path+'\\'+f.split('.')[0]+'\\'
    else:
        continue
    if not os.path.exists(directory):
        os.makedirs(directory)
    Archive(dir_path + '\\' + f).extractall(directory)


