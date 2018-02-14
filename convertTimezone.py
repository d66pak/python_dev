import pytz
from pytz import timezone

from dateutil.parser import parse
from dateutil import tz

import sys


def convertToTimezone1(fromDTStr, toTZStr):
    """
    This solution only requires dateutil package

    :param fromDTStr: Date string to convert like:  2018-02-01T15:50:35.000 or
                      2018-02-01T04:50:12Z
    :param toTZStr: Timezone string like: Australia/Sydney or UTC
    :return: from datetime, to datetime object
    """
    fromDT = parse(fromDTStr)
    # Check if timezone info is present else add local timezone
    if fromDT.tzinfo is None:
        fromDT = fromDT.replace(tzinfo=tz.gettz('Australia/Sydney'))

    # Convert to destination timezone
    return fromDT, fromDT.astimezone(tz.gettz(toTZStr))


def convertToTimezone2(fromDTStr, toTZStr):
    """
    This solution requires dateutil and pytz package

    :param fromDTStr: Date string to convert like:  2018-02-01T15:50:35.000 or
                      2018-02-01T04:50:12Z
    :param toTZStr: Timezone string like: Australia/Sydney or UTC
    :return: from datetime, to datetime object
    """
    fromDT = parse(fromDTStr)
    # Check if timezone info is present else add local timezone
    if fromDT.tzinfo is None:
        localTZ = timezone('Australia/Sydney')
        fromDT = localTZ.localize(fromDT, is_dst=True)

    # Convert to destination timezone
    return fromDT, fromDT.astimezone(timezone(toTZStr))


if __name__ == '__main__':
    dtStr = sys.argv[1]
    toTZStr = sys.argv[2]

    fromDT1, toDT1 = convertToTimezone1(dtStr, toTZStr)
    fromDT2, toDT2 = convertToTimezone2(dtStr, toTZStr)

    print 'Method 1 -->  ' + 'From\t' + str(fromDT1) + '\tTo\t' + str(toDT1)
    print 'Method 2 -->  ' + 'From\t' + str(fromDT2) + '\tTo\t' + str(toDT2)
