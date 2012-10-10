'''
Created on 10-Oct-2012

@author: arun
'''
from utils import readfiles
from utils import namedentityrecognizer as NER
rf = readfiles.readfile('/home/arun/Luke/part-m-00000')
data_map = rf.readData()
named_entities = NER.ner(data_map)
named_entities.identify_entities()