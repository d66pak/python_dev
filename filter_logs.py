import os
import boto3
import pdb
import time
from datetime import datetime
from datetime import timedelta
from botocore.compat import total_seconds


def main():
    aws_profile = 'default'
    os.environ['AWS_PROFILE'] = aws_profile
    # logs = boto3.session.Session(profile_name=aws_profile).client('logs')
    logs = boto3.client('logs', region_name='ap-southeast-2')

    start = datetime.utcnow() - timedelta(minutes=10)
    end = datetime.utcnow()

    print 'start', start, 'end', end

    start = int(time.mktime(start.timetuple())) * 1000
    end = int(time.mktime(end.timetuple())) * 1000

    kwargs = {
        'logGroupName': '/aws/lambda/CustomerSales',
        'interleaved': True,
        'startTime': start,
        'endTime': end,
        'startTime': int(total_seconds((datetime.utcnow() - timedelta(seconds=300)) - datetime(1970, 1, 1))) * 1000,
        'endTime': int(total_seconds(datetime.utcnow() - datetime(1970, 1, 1))) * 1000
    }

    cnt = 0
    while True:
        cnt += 1
        print '0--------0'
        print str(kwargs)
        d_response = logs.filter_log_events(**kwargs)
        print str(d_response)

        if d_response['events']:
            pdb.set_trace()
            print 'Finally got results after {0} atttempts'.format(cnt)
            break

        kwargs['nextToken'] = d_response['nextToken']


if __name__ == '__main__':
    main()
