"""
AWS Lambda to copy s3 object from source s3 bucket to Ali Cloud OSS (similar to s3 bucket).
Interestingly, boto3 can copy objects from AWS to Ali Cloud!

NOTE:
    - Lambda's trigger should be set as source S3 bucket so, any files coming in are notified to Lambda.
    - Environment variables:
        LOG_LEVEL: DEBUG or INFO or ERROR
"""
import os
import logging
import boto3
import gzip
from StringIO import StringIO

# Setup logging
LOG = logging.getLogger(__name__)
LOG.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

TO_BUCKET='hybrid-realtime-data'

S3 = boto3.client('s3')

OSS = boto3.client(
    service_name='s3',
    region_name='ap-southeast-2',
    endpoint_url='https://hybrid-realtime-data.oss-ap-southeast-2.aliyuncs.com',
    aws_access_key_id='LTAI6QWnQfe',
    aws_secret_access_key='ZuDMsEKjfJ3C0K2wJMV'
)


def lambda_handler(event, context):
    try:
        l_t_bucketKey = _getKeys(event)
        LOG.info('About to copy %d files', len(l_t_bucketKey))
        for bucket, key in l_t_bucketKey:
            try:
                inFileObj = StringIO()
                S3.download_fileobj(
                    Bucket=bucket,
                    Key=key,
                    Fileobj=inFileObj
                )
                # Reset read pos
                inFileObj.seek(0)

                # Uncompress
                compressedFileObj = gzip.GzipFile(fileobj=inFileObj, mode='rb')
                outFileObj = StringIO(compressedFileObj.read())

                # Extract table name from following string
                # priority-2-entities/staging.renewalinfo-i-0a2e93e36906e11b6_1541132540053.csv.gz
                # staging-orderlinepayment/staging.orderlinepayment_1541399167355_0.csv.gz
                # staging-orders-orderlineitems/staging.orders_orderlineitems_1541400392727_2.csv.gz
                fileName = os.path.basename(key)
                if '-i-' in fileName:
                    tableName = fileName.split('-i-')[0]
                else:
                    tableName = fileName[:-23]
                toKey = fileName[:-3]
                # LOG.debug('Bucket: %s Key: %s', bucket, key)
                # LOG.debug('FileName: %s TableName: %s ToKey: %s', fileName, tableName, toKey)
                OSS.upload_fileobj(Fileobj=outFileObj, Bucket=tableName, Key=toKey)

                LOG.debug('Copied s3://%s/%s to s3://%s/%s', bucket, key, tableName, toKey)
            except:
                LOG.exception('Error copying file: {k}'.format(k=key))
        return 'SUCCESS'
    except Exception as e:
        LOG.exception("Lambda function failed:")
        return 'ERROR'


def _getKeys(d_event):
    """
    Extracts (bucket, key) from event

    :param d_event: Event dict
    :return: List of tuples (bucket, key)
    """
    l_t_bucketKey = []
    if d_event:
        if 'Records' in d_event and d_event['Records']:
            for d_record in d_event['Records']:
                try:
                    bucket = d_record['s3']['bucket']['name']
                    key = d_record['s3']['object']['key']
                    l_t_bucketKey.append((bucket, key))
                except:
                    LOG.warn('Error extracting bucket and key from event')
    return l_t_bucketKey
