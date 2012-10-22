'''
Created on 19-Oct-2012

@author: arun
'''
import re
import logging
import codecs
from utils.constants import Month
from utils.matchers.ahocorasick.matcher import PatternMatcher

logger = logging.getLogger("Processor.identify_named_entities")
class Datetag:
    
    @classmethod
    def date_formatter(cls, sentence):
        date_identifier1 = u'(?<=[\s\.,])((\d\d)[\s\.-]{1,2}([\w]+?)[\s\.-]{1,2}(\d\d\d\d))(?=[\s\.,]|\Z)|'\
                           u'(?<=\A)((\d\d)[\s\.-]{1,2}([\w]+?)[\s\.-]{1,2}(\d\d\d\d))(?=[\s\.,]|\Z)'
        date_identifier2 = u'(?<=[\s\.,])((\d\d\d\d)[\s\.-]{1,2}(\d\d)[\s\.-]{1,2}(\d\d))(?=[\s\.,T]|\Z)|'\
                           u'(?<=\A)((\d\d\d\d)[\s\.-]{1,2}(\d\d)[\s\.-]{1,2}(\d\d))(?=[\s\.,T]|\Z)'
        date_identifier3 = u'(?:(?<=[\s\.,])|\A)((\d\d\d\d)(\d\d)(\d\d))(?=[\s\.,T]|\Z)'
        date1 = re.search(date_identifier1, sentence, flags=re.U|re.I)
        date2 = re.search(date_identifier2, sentence, flags=re.U|re.I)
        date3 = re.search(date_identifier3, sentence, flags=re.U|re.I)
        date_val = ''
        if date1:
            try:
                day = date1.groups()[1]
                month = Month.return_map_lookup(date1.groups()[2])
                year = date1.groups()[3]
                date_val = '%s/%s/%s'%(year, month, day)
                sentence = re.sub(date1.groups()[0], u'<date>%s</date> '%date_val, sentence, flags=re.U|re.I)
            except:
                day = date1.groups()[5]
                month = Month.return_map_lookup(date1.groups()[6])
                year = date1.groups()[7]
                date_val = '%s/%s/%s'%(year, month, day)
                sentence = re.sub(date1.groups()[4], u'<date>%s</date> '%date_val, sentence, flags=re.U|re.I)
                
        elif date2:
            try:
                day = date2.groups()[3]
                month = date2.groups()[2]
                year = date2.groups()[1]
                date_val = '%s/%s/%s'%(year, month, day)
                sentence = re.sub(date2.groups()[0], '<date>%s</date> '%date_val, sentence, flags=re.U|re.I)
            except:
                day = date2.groups()[7]
                month = date2.groups()[6]
                year = date2.groups()[5]
                date_val = '%s/%s/%s'%(year, month, day)
                sentence = re.sub(date2.groups()[4], u'<date>%s</date> '%date_val, sentence, flags=re.U|re.I)
        elif date3:
            try:
                day = date3.groups()[3]
                month = date3.groups()[2]
                year = date3.groups()[1]
                date_val = '%s/%s/%s'%(year, month, day)
                sentence = re.sub(date3.groups()[0], '<date>%s</date> '%date_val, sentence, flags=re.U|re.I)
            except:
                logger.error('Date3 match not identified.. bailing out')
        return sentence

class Timetag:
    
    @classmethod
    def time_formatter(cls, sentence):
        time_identifier = u'(?:(?<=[\s\.,T])|\A)(\d\d:\d\d(:\d\d)*[\s\.,+]*(UTC|GMT|CEST|EDT|IST|BST|MSK)*(\d\d:\d\d)*)(?=[\s\n\.,T]|\Z)'
        #time_identifier = u'(?<=[\s\.,T])([\d]{2}[:]{1}[\d]{2}([:]{1}[\d]{2})*[\s\.,+]*(UTC|GMT|CEST|EDT|IST|BST)*(\d\d:\d\d)*)(?=[\s\.,T]|\Z)|'\
        #                  u'(?<=\A)([\d]{2}[:]{1}[\d]{2}([:]{1}[\d]{2})*[\s\.,+]*(UTC|GMT|CEST|EDT|IST|BST)*(\d\d:\d\d)*)(?=[\s\.,T]|\Z)'
        time = re.search(time_identifier, sentence, flags=re.U|re.I)
        if time:
            try:
                sentence = re.sub(u'(?:(?<=[\s\.,T])|\A)%s(?=[\s\n\.,]|\Z)'%time.groups()[0], u'<time>%s</time>'%time.groups()[0], sentence, flags=re.U|re.I)
            except:
                logger.error('Time not identified... aborting')
                return sentence
        return sentence

class URLtag:
    
    @classmethod
    def url_formatter(cls, sentence):
        url_identifier = u'(?:(?<=[\s\d\.,])|\A)(^((ht|f)tp(s?)\:\/\/|~/|/)?([\w]+:\w+@)?([a-zA-Z]{1}([\w\-]+\.)+([\w]{2,5}))(:[\d]{1,5})?((/?\w+/)+|/?)(\w+\.[\w]{3,4})?((\?\w+=\w+)?(&\w+=\w+)*))(?=[\s\n\.,]|\Z)'
        url = re.search(url_identifier, sentence, flags=re.U|re.I)
        if url:
            try:
                sentence = re.sub('(?:(?<=[\s\.,])|\A)%s(?=[\s\n\.,]|\Z)'%url.groups()[0], u'<url>%s</url>'%url.groups()[0], sentence, flags=re.U|re.I)
            except:
                logger.error('URL not identified... aborting')
                return sentence
        return sentence

class Emailtag:
    
    @classmethod
    def email_formatter(cls, sentence):
        email_identifier = u'(?:(?<=[\s\.,])|\A)([a-zA-Z0-9+_\-\.]+@[0-9a-zA-Z][.-0-9a-zA-Z]*.[a-zA-Z]+)(?=[\s\n\.,]|\Z)'
        email = re.search(email_identifier, sentence, flags=re.U|re.I)
        if email:
            try:
                sentence = re.sub(ur'(?:(?<=[\s\.,])|\A)%s(?=[\s\n\.,]|\Z)'%email.groups()[0], ur'<email>%s</email>'%email.groups()[0], sentence, flags=re.U|re.I)
            except:
                logger.error('Email not identified... aborting')
                return sentence
        return sentence
    
class IPtag:
    
    @classmethod
    def ip_formatter(cls, sentence):
        ip_identifier = u'(?:(?<=[\s\.,])|\A)((?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}))(?=[\s\n\.,]|\Z)'
        ip = re.search(ip_identifier, sentence, flags=re.U|re.I)
        if ip:
            try:
                sentence = re.sub(ur'(?:(?<=[\s\.,])|\A)%s(?=[\s\n\.,]|\Z)'%ip.groups()[0], u'<ip_addr>%s</ip_addr>'%ip.groups()[0], sentence, flags=re.U|re.I)
            except:
                logger.error('IP address not identified... aborting')
                return sentence
        return sentence

class Phonetag:
    
    @classmethod
    def phone_formatter(cls, sentence):
        phone_identifier = u'(^(?:(?:\+?\d{1,2}\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{3,6})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$)'
        phone = re.search(phone_identifier, sentence, flags=re.U|re.I)
        if phone:
            try:
                if '+' not in phone.groups()[0]:
                    sentence = re.sub(r'(?:(?<=[\s\.,])|\A)%s(?=[\s\n\.,$]|\Z)'%phone.groups()[0], ur'<phone_no>%s</phone_no>'%phone.groups()[0], sentence, flags=re.U|re.I)
                else:
                    sentence = re.sub(r'(?:(?<=[\s\.,])|\A)\%s(?=[\s\n\.,$]|\Z)'%phone.groups()[0], ur'<phone_no>%s</phone_no>'%phone.groups()[0], sentence, flags=re.U|re.I)
            except:
                logger.error('Phone number not identified... aborting')
                return sentence
        return sentence

class Countrytag:
    
    @classmethod
    def country_formatter(cls, sentence, countries, split_sentence):
        country_identified = ''
        company_context = set([u'ltd', u'ltd.', u'llc.', u'llc', u'pty', u'pty.', u'private',\
                               u'public', u'inc', u'inc.', u'company', u'company.', u'limited',\
                               u'limited.', u'plc', u'plc.'])
        
        # if company context identified, do not identify as country
        def check_context(pos, sent_list):
            length = len(sent_list)
            if pos<length-1:
                for i in range(pos+1,length-1):
                    if sent_list[i].strip().lower() in company_context:
                        return True
            return False          
            
        for i,items in enumerate(split_sentence):
            if items.lower() in countries:
                country_identified = items
                if check_context(i, split_sentence):
                    return sentence
                else:
                    sentence = re.sub(country_identified,'<country>%s</country>'%country_identified.upper(), sentence, flags=re.U|re.I)
        return sentence

class Citiestag:
    
    @classmethod
    def cities_tagger(cls, sentence, cities, split_sentence):
        cities_identified = ''
        company_context = set([u'ltd', u'ltd.', u'llc.', u'llc', u'pty', u'pty.', u'private',\
                               u'public', u'inc', u'inc.', u'company', u'company.', u'limited',\
                               u'limited.', u'plc', u'plc.'])
        
        # if company context identified, do not identify as country
        def check_context(pos, sent_list):
            length = len(sent_list)
            if pos<length-1:
                for i in range(pos+1,length-1):
                    if sent_list[i].strip().lower() in company_context:
                        return True
            return False
        
        for i,items in enumerate(split_sentence):
            if items.lower() in cities:
                cities_identified = items
                if check_context(i, split_sentence):
                    return sentence
                else:
                    sentence = re.sub(cities_identified,'<city>%s</city>'%cities_identified.upper(), sentence, flags=re.U|re.I)
        return sentence

class 