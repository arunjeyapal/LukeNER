# -*- coding: utf8 -*-
'''
Created on 19-Oct-2012

@author: arun
'''

class Month:
    months = {
              u'jan':1,
              u'january':1,
              u'feb':2,
              u'february':2,
              u'mar':3,
              u'march':3,
              u'apr':4,
              u'april':4,
              u'may':5,
              u'jun':6,
              u'june':6,
              u'jul':7,
              u'july':7,
              u'aug':8,
              u'august':8,
              u'sep':9,
              u'september':9,
              u'oct':10,
              u'october':10,
              u'nov':11,
              u'november':11,
              u'dec':12,
              u'december':12,
              }
    
    @classmethod
    def return_mapkeys(cls):
        return set(cls.months.keys())
    
    @classmethod
    def return_map_lookup(cls, key):
        if key.lower() not in cls.months:
            return 0
        else:
            return cls.months[key.lower()]
