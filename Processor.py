'''
Created on 10-Oct-2012

@author: arun
'''
import cPickle
import codecs
from utils import readfiles
from utils.perf_tools import calc_time
from utils import split_data
import logging.handlers

class processor:
    logger = logging.getLogger('Processor')
    
    def setup_logger(self):
        DEBUG_LOG_FILENAME = 'log_data/debug.log'
        log = logging.getLogger('Processor')
        # set level
        log.setLevel(logging.DEBUG)
        # create handlers
        debug_handler = logging.handlers.RotatingFileHandler(
            DEBUG_LOG_FILENAME, mode='a', maxBytes=4096 * 1024, backupCount=5)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        #create formatter
        formatter = logging.Formatter('%(asctime)s - %(funcName)s (%(lineno)s) [%(levelname)s] %(message)s')
        plain_formatter = logging.Formatter('%(message)s')
        #attach formatter to handlers
        debug_handler.setFormatter(formatter)
        console_handler.setFormatter(plain_formatter)
        #attach handlers to logger
        log.addHandler(debug_handler)
        log.addHandler(console_handler)
        return log
    
    def __init__(self):
        global logger
        logger = self.setup_logger()
        # if pickle file identified
        # Countries list is serialized as a set
        self.country = set()
        self.city = set()
        
        try:
            self.country = cPickle.load(open('data/countries.pkl','rU'))
        except IOError:
            countries_lst = codecs.open('data/countries.lst', 'rU', 'utf8') 
            for items in countries_lst:
                self.country.add(items.strip().lower())
            cPickle.dump(self.country, open('data/countries.pkl', 'w'))
        
        try:
            self.city = cPickle.load(open('data/cities.pkl','rU'))
        except IOError:
            cities_lst = codecs.open('data/cities.lst', 'rU', 'utf8') 
            for items in cities_lst:
                self.city.add(items.strip().lower())
            cPickle.dump(self.city, open('data/cities.pkl', 'w'))
    
    @calc_time
    def process(self):
        rf = readfiles.readfile('/home/arun/Luke/part-m-00000')
        data_map = rf.readData()
        logger.info('Data read successful')
        named_entities = split_data.split_data(data_map, self.country)
        named_entities.identify_entities()
        
processor = processor()
processor.process()