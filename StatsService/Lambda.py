import os
import time
import logging

from StatsService import StatsService

# Setup logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.ERROR)
# LOG.addHandler(logging.StreamHandler())


def lambda_handler(event, context):
    try:
        function_name = os.environ['AWS_LAMBDA_FUNCTION_NAME']
        lm = Lambda(function_name, context)
        lm.log()
        return 'SUCCESS'
    except Exception as e:
        LOG.exception("Lambda function failed:")
        return 'ERROR'


class Lambda(object):
    def __init__(self, function_name, context):
        self.function_name = function_name
        # Set proper log level from config
        LOG.setLevel(logging.getLevelName('DEBUG'))

        # Setup StatsService
        self.ss = StatsService(function_name, LOG)

    def log(self):
        LOG.debug("---- Testing ----")
        time.sleep(1)
        LOG.info("---- Testing ----")
        time.sleep(1)
        LOG.warning("---- Testing ----")
        time.sleep(1)
        LOG.critical("---- Testing ----")

        self.ss.monitor(
            metric_name='Mon_metric_1',
            metric_value=2
        )
        self.ss.monitor(
            metric_name='Mon_metric_1',
            metric_value=3,
            d_tags={'tagA': 'A', 'tagB': 'B'}
        )

        self.ss.diagnose(
            message='>>>>>>> Testing <<<<<<<<',
            metric_name='Dia_1'
        )
        self.ss.diagnose(
            message='>>>>>>> Testing {} <<<<<<<<'.format(1),
            metric_name='Dia_2',
            d_tags={'tagA': 'A', 'tagB': 'B'}
        )


def main():
    """ This function use only for the local env execution. """
    os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'Lambda'
    lambda_handler(None, None)


if __name__ == '__main__':
    main()
