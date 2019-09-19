from datetime import datetime

METRIC_TYPE_COUNT = 'c'
METRIC_TYPE_TIMER = 'ms'


class StatsService(object):
    """
    Class to log diagnostic and monitoring messages in a pre determined format.
    """

    DT_FORMAT = '%Y-%m-%d %H:%M:%S,%f'
    MONITOR_FORMAT = '|{stat_type}|{metric_value}|{metric_type}|{metric_name}|{metric_timestamp}|{tags}|'
    DIAGNOSE_FORMAT = '|{stat_type}|"{message}"|{metric_name}|{metric_timestamp}|{tags}|'

    def __init__(self, function_name, logger):
        self.function_name = function_name
        self.logger = logger

    def _build_tags(self, d_tags):
        if d_tags is None:
            d_tags = {'function_name': self.function_name}
        else:
            d_tags['function_name'] = self.function_name
        return '#'+', '.join(['{}: {}'.format(tag, value) for (tag, value) in d_tags.iteritems()])

    def monitor(self, metric_name, metric_value=1, metric_type=METRIC_TYPE_COUNT, metric_timestamp=datetime.now(), d_tags=None):
        """
        Logs a 'MONITORING' line

        :param metric_name:      Name of the metric.
        :param metric_value:     (optional) Numerical value if METRIC_TYPE_COUNT else value in seconds if METRIC_TYPE_TIMER.
                                            Default is 1.
        :param metric_type:      (optional) METRIC_TYPE_COUNT (default) or METRIC_TYPE_TIMER
        :param metric_timestamp: (optional) Metric datetime if different that datetime.now()
        :param d_tags:           (optional) Dict of tags. Eg. {'tagA': 'A', 'tagB', 'B'}.
                                            By default {'function_name': '<lambda_function_name>' is added.
        :return: None
        """
        if metric_type == METRIC_TYPE_TIMER:
            metric_value *= 1000  # convert to milliseconds

        self.logger.info(StatsService.MONITOR_FORMAT.format(
            stat_type='MONITORING',
            metric_name=metric_name,
            metric_value=metric_value,
            metric_type=metric_type,
            metric_timestamp=metric_timestamp.strftime(StatsService.DT_FORMAT)[:-3],
            tags=self._build_tags(d_tags)
        ))

    def diagnose(self, message, metric_name, metric_timestamp=datetime.now(), d_tags=None):
        """
        Logs a 'DIAGNOSTIC' line

        :param message:          Diagnostic message.
        :param metric_name:      Name of the metric.
        :param metric_timestamp: (optional) Metric datetime if different that datetime.now()
        :param d_tags:           (optional) Dict of tags. Eg. {'tagA': 'A', 'tagB', 'B'}.
                                            By default {'function_name': '<lambda_function_name>' is added.
        :return: None
        """
        self.logger.info(StatsService.DIAGNOSE_FORMAT.format(
            stat_type='DIAGNOSTIC',
            message=message,
            metric_name=metric_name,
            metric_timestamp=metric_timestamp.strftime(StatsService.DT_FORMAT)[:-3],
            tags=self._build_tags(d_tags)
        ))
