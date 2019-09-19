"""
AWS Lambda to copy s3 object from source s3 bucket to destination s3 bucket.

NOTE:
    - Lambda's trigger should be set as source S3 bucket so, any files coming in are notified to Lambda.
    - Environment variables:
        TO_BUCKET: Name of the destination S3 bucket
        TO_DIR: Directory inside s3 bucket
        LOG_LEVEL: DEBUG or INFO or ERROR
"""
import os
import logging
import boto3

# Setup logging
LOG = logging.getLogger(__name__)
LOG.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

S3 = boto3.client('s3')


def lambda_handler(event, context):
    ipps = None
    try:
        l_t_bucketKey = _getKeys(event)
        LOG.info('About to copy %d files', len(l_t_bucketKey))
        for bucket, key in l_t_bucketKey:
            try:
                copy_source = {'Bucket': bucket, 'Key': key}
                if os.environ['TO_DIR']:
                    toKey = os.environ['TO_DIR'] + '/' + key
                else:
                    toKey = key
                S3.copy(copy_source, os.environ['TO_BUCKET'], toKey)
                LOG.debug('Copied s3://%s/%s', bucket, key)
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