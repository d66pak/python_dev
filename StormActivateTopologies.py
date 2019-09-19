"""
Activate all the Storm topologies.

USAGE: python StormActivateTopologies.py <storm_ui_host_port>

Example: python StormActivateTopologies.py http://10.1.2.3:8080

Crontab example: Assuming this script is present at location /home/ubuntu/storm_activate_deactivate

0 1 * * * cd /home/ubuntu/storm_activate_deactivate; python StormActivateTopologies.py http://10.1.2.3:8080 &
"""
import sys
import json
import urllib
import urllib2
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = 'activate.log'
STORM_TOPOLOGY_SUMMARY = '/api/v1/topology/summary'
STORM_TOPOLOGY_ACTIVATE = '/api/v1/topology/{topology_id}/activate'

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')
fh = RotatingFileHandler(LOG_FILE_NAME, maxBytes=1024*10, backupCount=5)
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
LOG.addHandler(fh)


def main():
    if len(sys.argv) < 2:
        LOG.error('Missing command line argument: StormUI host:port')
        sys.exit(1)

    storm_ui_serverport = sys.argv[1]
    summaryUrl = storm_ui_serverport + STORM_TOPOLOGY_SUMMARY
    data = urllib2.urlopen(urllib2.Request(summaryUrl)).read()
    try:
        if data:
            d_data = json.loads(data)
            if 'topologies' in d_data and d_data['topologies']:
                for d_topology in d_data['topologies']:
                    url = storm_ui_serverport + STORM_TOPOLOGY_ACTIVATE.format(topology_id=d_topology['id'])
                    LOG.info('Activating: %s', url)
                    req = urllib2.Request(url, urllib.urlencode({}))
                    urllib2.urlopen(req)
            else:
                LOG.error('No topologies found to activate.')
        else:
            LOG.error('No response returned by GET: %s', summaryUrl)
    except:
        LOG.exception('ERROR: ')


if __name__ == '__main__':
    main()
