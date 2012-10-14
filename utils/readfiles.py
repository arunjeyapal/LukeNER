'''
Created on 10-Oct-2012

@author: arun
'''
import logging

logger = logging.getLogger('Processor.readfiles')
class readfile:
    
    def __init__(self, filename):
        self.filename = filename
        self.fileopen = open(self.filename,'rU')
    
    def split_whois_text(self, sentence):
        sent_list = sentence.split('%0A')
        return sent_list
        
    def readData(self):
        data = {}
        for lines in self.fileopen:
            try:
                domain, scraper_internal_dns, scraper_ip, unixtime, whois_text, dig_text, failed  = lines.split("\t")
                data[domain.lower()] = [self.split_whois_text(whois_text),unixtime]
            except Exception:
                logger.warning("Couldn't Parse:"+lines.strip())
                continue
        return data