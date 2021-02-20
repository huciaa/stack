import pandas as pd
import xml.etree.ElementTree as et
import csv
import os

path = r'/home/ec2-user'

dir_path = os.path.dirname(os.path.realpath(__file__))
directories = [f for f in os.walk(os.path.join(path, 'unpack'))]

for f in directories[1:]:
    print(f)
    dataset = os.path.basename(str(f[0]))
    for files in f[2]:

        if 'Badges' in files and 1:
            xml_path = os.path.join(str(f[0]), files)

            xtree = et.parse(xml_path)
            xroot = xtree.getroot()

            df_cols = ["UserId", "Name", "Date", 'Class', 'TagBased', 'Dataset']
            rows = []
            dir = os.path.join(path, 'data', 'badges', dataset)
            if not os.path.exists(dir):
                os.makedirs(dir)

            file = open(os.path.join(dir, 'badges.csv'), 'w', newline='', encoding="utf-8")
            with file:
                write = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                write.writerow(df_cols)
                for node in xroot:
                    s_Id = node.attrib.get("UserId")
                    rows.append(s_Id)
                    s_Name = node.attrib.get("Name")
                    rows.append(s_Name)
                    s_Date = node.attrib.get("Date")
                    rows.append(s_Date)
                    s_Class = node.attrib.get("Class")
                    rows.append(s_Class)
                    s_TagBased = node.attrib.get("TagBased")
                    rows.append(s_TagBased)
                    write.writerow(rows + [dataset])
                    rows = []
        if 'Comments' in files and 0:
            xml_path = os.path.join(str(f[0]), files)

            xtree = et.parse(xml_path)
            xroot = xtree.getroot()

            df_cols = ["PostId", "Score", "Text", 'CreationDate', 'UserId','ContentLicense', 'Dataset']
            rows = []

            file = open(os.path.join(path+'/data/comments.csv'), 'a', newline='', encoding="utf-8")
            with file:
                write = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
                write.writerow(df_cols)
                for node in xroot:
                    s_PostId = node.attrib.get("PostId")
                    rows.append(s_PostId)
                    s_Score = node.attrib.get("Score")
                    rows.append(s_Score)
                    s_Text = node.attrib.get("Text").replace('\n', ' ').replace('|', ',')
                    rows.append(s_Text)
                    s_CreationDate = node.attrib.get("CreationDate")
                    rows.append(s_CreationDate)
                    s_UserId = node.attrib.get("UserId")
                    rows.append(s_UserId)
                    s_ContentLicense = node.attrib.get("ContentLicense")
                    rows.append(s_ContentLicense)
                    write.writerow(rows+[dataset])
                    rows = []

