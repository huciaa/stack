import json
import urllib.parse
import boto3
import xml.etree.ElementTree as et
from xml.etree.ElementTree import fromstring, ElementTree
import csv
import os
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import time
import datetime

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    destination_bucket = boto3.resource('s3').Bucket('stackdev2prq')
    try:
        print(key)
        if 'Badges' in key:
            table = 'Badges'
            df_cols = ["Id", "PostId", "Score", "Text", 'CreationDate', 'UserId', 'ContentLicense', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        if 'Comments' in key:
            table = 'Comments'
            df_cols = ["PostId", "Score", "Text", 'CreationDate', 'UserId', 'ContentLicense', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        if 'Posts' in key:
            table = 'Posts'
            df_cols = ["Id", "PostTypeId", "AcceptedAnswerId", 'CreationDate', 'Score', 'ViewCount', 'Body',
                       'OwnerUserId', 'LastEditorUserId', 'LastEditorDisplayName',
                       'LastEditDate', 'LastActivityDate', 'CommunityOwnedDate', 'ClosedDate', 'Title', 'Tags',
                       'AnswerCount', 'CommentCount', 'FavoriteCount', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        if 'PostHistory' in key:
            table = 'PostHistory'
            df_cols = ["Id", "PostHistoryTypeId", "PostId", 'RevisionGUID', 'CreationDate', "UserId", "UserDisplayName",
                       'Comment', 'Text', 'CloseReasonId', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        if 'PostLinks' in key:
            table = 'PostLinks'
            df_cols = ["Id", "CreationDate", "PostId", 'RelatedPostId', 'UserId', 'ContentLicense', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        if 'Users' in key:
            table = 'Users'
            df_cols = ["Id", "Reputation", "CreationDate", 'DisplayName', 'EmailHash', 'LastAccessDate', 'WebsiteUrl',
                       'Location', 'Age', 'AboutMe',
                       'Views', 'UpVotes', 'DownVotes', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)
        if 'Votes' in key:
            table = 'Votes'
            df_cols = ["Id", "PostId", "VoteTypeId", 'CreationDate', 'UserId', 'BountyAmount', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)
        if 'Tags' in key:
            table = 'Tags'
            df_cols = ["Id", 'TagName', 'Count', 'ExcerptPostId', 'WikiPostId', 'IsModeratorOnly',
                       'IsRequired', 'Dataset']

            parse_file(bucket, key, table, df_cols, destination_bucket)

        return 'ok'
    except Exception as e:
        print(e)
        print(
            'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(
                key, bucket))
        raise e


def get_root(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    xmldata = response['Body'].read().decode('utf-8')
    tree = ElementTree(fromstring(xmldata))
    root = tree.getroot()
    return root


def parse_file(bucket, key, table, df_cols, destination_bucket):
    root = get_root(bucket, key)
    frame = []
    rows = []
    dataset = key.split('/')[0]
    batch = key.split('/')[-1].split('.')[0]
    filename = batch + '_' + dataset + '.prq'

    for node in root:
        for a in df_cols[:-1]:
            val = str(node.attrib.get(a))
            if val != 'None':
                try:
                    val = val.replace('\n', ' ')
                except:
                    pass
                try:
                    val = val.replace('|', ',')
                except:
                    pass
                try:
                    val = val.replace('&#xD;&#xA;', '')
                except:
                    pass
                try:
                    val = val.replace('\r', '')
                except:
                    pass
                try:
                    val = val.replace('"', '')
                except:
                    pass
                if len(val) > 0 and val[-1] == chr(92):
                    val = val + ' '
                if a == 'Date' or a == 'CreationDate' or a == 'LastEditDate' or a == 'LastActivityDate' or a == 'CommunityOwnedDate' or a == 'ClosedDate' or a == 'LastAccessDate':
                    val = str(int(time.mktime(datetime.datetime.fromisoformat(val).timetuple()))) + '000'
            else:
                val = ''
            rows.append(val)
        rows.append(dataset)
        frame.append(rows)
        rows = []

    df = pd.DataFrame(frame, columns=df_cols)
    file_pq = pa.Table.from_pandas(df, preserve_index=True)
    pq.write_table(file_pq, '/tmp/'+filename)
    destination_bucket.upload_file(os.path.join('/tmp/', filename), os.path.join(table, filename))
    print(os.path.join('/tmp/', filename) + ' uploaded to ' + os.path.join(table, filename))

