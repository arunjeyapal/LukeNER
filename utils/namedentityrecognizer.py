'''
Created on 10-Oct-2012

@author: arun
'''
class ner:
    def __init__(self, data):
        self.whois_text = data
        self.domains = self.whois_text.keys()
    
    def identify_entities(self):
        for each_domain in self.domains:
            whois_list =  self.whois_text[each_domain.lower()][0]
            unix_timestamp = self.whois_text[each_domain.lower()][1]
            for each_item in whois_list:
                print each_item
            
    def write_tofile(self, domain, whois_key, whois_value, unix_timestamp):
        "hello"