import json
import urllib
import urllib2
import logging
from logging.handlers import RotatingFileHandler

LOG_FILE_NAME = 'deactivate.log'
STORM_UI_SERVERPORT = 'http://10.123.0.29:8080'
STORM_TOPOLOGY_SUMMARY = '/api/v1/topology/summary'
STORM_TOPOLOGY_ACTIVATE = '/api/v1/topology/{topology_id}/activate'
STORM_TOPOLOGY_DEACTIVATE = '/api/v1/topology/{topology_id}/deactivate'

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')
LOG.addHandler(RotatingFileHandler(LOG_FILE_NAME, maxBytes=1024*10, backupCount=5))


def main():
    summaryUrl = STORM_UI_SERVERPORT + STORM_TOPOLOGY_SUMMARY
    data = urllib2.urlopen(urllib2.Request(summaryUrl)).read()
    try:
        if data:
            d_data = json.loads(data)
            if 'topologies' in d_data and d_data['topologies']:
                for d_topology in d_data['topologies']:
                    url = STORM_UI_SERVERPORT + STORM_TOPOLOGY_DEACTIVATE.format(topology_id=d_topology['id'])
                    LOG.info('Deactivating: %s', url)
                    req = urllib2.Request(url, urllib.urlencode({}))
                    urllib2.urlopen(req)
            else:
                LOG.error('No topologies found to deactivate.')
        else:
            LOG.error('No response returned by GET: %s', summaryUrl)
    except:
        LOG.exception('ERROR: ')


if __name__ == '__main__':
    main()
