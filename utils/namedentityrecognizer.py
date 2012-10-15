'''
Created on 10-Oct-2012

@author: arun
'''
import re
import logging

logger = logging.getLogger("Processor.namedentityrecognizer")
class ner:
    def __init__(self, data):
        self.whois_text = data
        self.domains = self.whois_text.keys()
    
    def identify_entities(self):
        all_entities = self.get_key_value_entities()
        self.filter_keyvalue_pairs(all_entities)
        
    def get_key_value_entities(self):
        logger.info("parsing Whois text to identify words which has ':' in it")
        key_value_regex = u'(?<=\s)([\s\w]+?)\:([^/]+[\s\w\W]+)(?=[\s\.,]|\Z)|'\
                          u'(?<=\A)([\s\w]+?)\:([^/]+[\s\w\W]+)(?=[\s\.,]|\Z)'
        all_text = []
        for each_domain in self.domains:
            whois_list =  self.whois_text[each_domain.lower()][0]
            unix_timestamp = self.whois_text[each_domain.lower()][1]
            key_value_entities = []
            for each_item in whois_list:
                key_value_pair = re.search(key_value_regex, each_item, flags=re.IGNORECASE)
                if key_value_pair:
                    try:
                        key_value_entities.append((key_value_pair.groups()[0].strip(), key_value_pair.groups()[1].strip()))
                    except AttributeError:
                        key_value_entities.append((key_value_pair.groups()[2].strip(), key_value_pair.groups()[3].strip()))
            all_text.append((each_domain, key_value_entities, unix_timestamp))
        logger.info("Identified text which has ':' colon in them")
        return all_text
    
    def filter_keyvalue_pairs(self, all_entities):
        logger.info("Filtering key_value entities")
        for each_list in all_entities:
            domain, key_value_list, timestamp = each_list
            for (key, value) in key_value_list:
                key = re.sub(' ', '_', key,flags=re.IGNORECASE)
                print '%s\twhois.%s\t%s'% (domain, key.lower(), timestamp), value
                
    def write_tofile(self, domain, whois_key, whois_value, unix_timestamp):
        "hello"