import sys
import fcntl
import zc.lockfile
import os
from os import path


def lock1():
    """
    NOT WORKING
    """
    lockFile = path.join('/home/deepakt', 'Documents/dev/python_dev', 'locktest.lock')
    try:
        lock = zc.lockfile.LockFile(lockFile, content_template='{pid};{hostname}')
        print 'Successfully acquired lock on: {filename}'.format(filename=lockFile)
    except zc.lockfile.LockError:
        print 'Error acquiring lock on: {filename}'.format(filename=lockFile)
        print '---- Shutting down ----'
        sys.exit(1)


def lock2():
    """
    WORKING
    """
    print '---- lock2 ----'
    lockFile = path.join('/home/deepakt', 'Documents/dev/python_dev', 'locktest.lock')
    try:
        fd = os.open(lockFile, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print 'Successfully acquired lock on: {filename}'.format(filename=lockFile)
    except Exception as e:
        print e.message
        print 'Error acquiring lock on: {filename}'.format(filename=lockFile)
        print '---- Shutting down ----'
        sys.exit(1)


def main():
    lock2()
    while True:
        pass


if __name__ == '__main__':
    main()
