import time
import sys

def pprint_unix_time(unix_time):
	
	return time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime(unix_time))

class Timer(object):
    '''Class that can be used measure timing using system clock'''
    def __init__(self, name = None):
        self.name = name

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        sys.stdout.write('-> %s [elapsed: %.2f s]\n' % (self.name, time.time() - self.tstart))
	