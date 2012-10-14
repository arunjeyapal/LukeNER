'''
Created on 10-Oct-2012

@author: arun
'''
import logging
import time

logger = logging.getLogger('Processor.calctime')

def calc_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        finish = time.time()
        #logger.info('function: [%s] Time:[%s] ms %s' % (func.__name__, (finish - start) * 1000, args))
        logger.debug('function: [%s] Time:[%s] ms' % (func.__name__, (finish - start) * 1000))
        return retval
    return wrapper