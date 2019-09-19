import os
import sys
import gzip
import json
import time
# import pdb
import boto3
import base64
from StringIO import StringIO

PROFILE_NAME = 'tkt_prod_ro'
S3_BUCKET = 'prod.au.vista.backup'
PREFIX = 'seatstatus/2018-02-14/'
OUT_DIR = 'seatstatus-2018-02-14'


def decode_data(data):
    b64decoded = base64.b64decode(data)
    return json.loads(gzip.GzipFile(fileobj=StringIO(b64decoded), mode='rb').read())


def main():
    # List out the files in S3 bucket
    s3 = boto3.session.Session(profile_name=PROFILE_NAME).client('s3')
    # s3 = boto3.session.Session(profile_name=PROFILE_NAME).resource('s3')
    # bucket = s3.Bucket(S3_BUCKET)

    while True:
        kwargs = {
            'Bucket': S3_BUCKET,
            'Prefix': PREFIX
        }
        d_response = s3.list_objects_v2(**kwargs)
        # print str(d_response['IsTruncated'])

        if 'Contents' in d_response and d_response['Contents']:
            for d_content in d_response['Contents']:
                try:
                    key = d_content['Key']
                    sys.stdout.write('\r%s' % key)
                    sys.stdout.flush()
                    in_file_obj = StringIO()
                    s3.download_fileobj(
                        Bucket=S3_BUCKET,
                        Key=key,
                        Fileobj=in_file_obj
                    )
                    in_file_obj.seek(0)
                    d_payload = json.loads(in_file_obj.read())
                    d_data = decode_data(d_payload['Data'])
                    outFileName = os.path.join(OUT_DIR, os.path.basename(key))
                    with open(outFileName, 'w') as fh:
                        fh.write(json.dumps(d_data) + '\n')
                except Exception as e:
                    print 'Exception: ' + e.message
        else:
            print 'No content found!'

        """
        NOTE: list_objects_v2 is sending 'isTruncated' as True but returning the same
        files in the second call. This will result is infinite loop. So, break!!
        """
        break

        # Check if the response was truncated
        if 'IsTruncated' in d_response and d_response['IsTruncated']:
            if 'NextContinuationToken' in d_response and d_response['NextContinuationToken']:
                kwargs['ContinuationToken'] = d_response['NextContinuationToken']
            else: break
        else: break

if __name__ == '__main__':
    main()
