from __future__ import print_function

import gzip
import json
import base64
from StringIO import StringIO

print('Loading function')


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        # print('record: ' + str(record))
        print(record['recordId'])
        payload = base64.b64decode(record['data'])
        print('payload: ' + str(payload))

        d_metadata = record.get('kinesisRecordMetadata', {})

        try:
            d_data = json.loads(gzip.GzipFile(fileobj=StringIO(payload), mode='rb').read())
            d_data.update(d_metadata)  # Add metadata to record

            # NOTE: not needed, payload will be compressed by kinesis firehose if compress is enabled
            # Compress data
            # file_obj = StringIO()
            # with gzip.GzipFile(fileobj=file_obj, mode='w') as gzipped_file:
            #     gzipped_file.write(json.dumps(d_data) + '\n')

            # Creted output record
            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(json.dumps(d_data) + '\n')
            }
        except Exception as e:
            print(e.message)
            # TODO: Handle the case where record cannot be transformed

        output.append(output_record)

    print('Successfully processed {} records.'.format(len(event['records'])))

    return {'records': output}
