#!/usr/bin/python

import sys
import base64
import gzip
from StringIO import StringIO

print gzip.GzipFile(fileobj=StringIO(base64.b64decode(sys.stdin.readline())), mode='rb').read()

