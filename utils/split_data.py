'''
Created on 10-Oct-2012

@author: arun
'''
import re
import logging
from utils.identify_named_entitites import Datetag, Timetag, URLtag, Emailtag,\
    IPtag, Phonetag, Countrytag

logger = logging.getLogger("Processor.namedentityrecognizer")
class split_data:
    def __init__(self, data, country):
        self.whois_text = data
        self.domains = self.whois_text.keys()
        self.countries = country
        
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
                self.identify_keyentities_keyvalue_pairs(value)
#                print '%s\twhois.%s\t%s\t%s'% (domain, key.lower(), value, timestamp)
        logger.info('key value pairs are identified')
    
    def tokenize(self, sentence):
        words = sentence.strip().split(' ')
        word_list = []
        new_word_list = []
        new_word_list2 = []
        pattern1 = u'(\w{2,}?|\d)(\.|,|\?|\!)\Z'
        pattern2 = u'(\w+?)(n\'t|\'m|\'ll|\'re|\'ve|\'d|\'s)'
        pattern3 = u'(?<!>)(\d{1,2})(:)(\d{1,2})(?!<)'
        for word in words:
            token = re.match(pattern1, word)
            # keep abbr intact
            if token and not re.search('[A-Z]\Z', token.group(1)):
                word_list.append(token.group(1))
                word_list.append(token.group(2))
            else:
                word_list.append(word)
        for word in word_list:
            matched = re.match(pattern2, word)
            if matched:
                new_word_list.append(matched.group(1))
                new_word_list.append(matched.group(2))
            else:
                new_word_list.append(word)
        for word in new_word_list:
            matched = re.match(pattern3, word)
            if matched:
                new_word_list2.append(matched.group(1))
                new_word_list2.append(matched.group(2))
                new_word_list2.append(matched.group(3))
            else:
                new_word_list2.append(word)
        return new_word_list2
                
    def identify_keyentities_keyvalue_pairs(self, values):
        values = Datetag.date_formatter(values)
        values = Timetag.time_formatter(values)
        values = URLtag.url_formatter(values)
        values = Emailtag.email_formatter(values)
        values = IPtag.ip_formatter(values)
        values = Phonetag.phone_formatter(values)
        values = Countrytag.country_formatter(values, self.countries, self.tokenize(values))
                
    def write_tofile(self, domain, whois_key, whois_value, unix_timestamp):
        "hello"