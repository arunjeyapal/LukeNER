__author__ = 'luke'
import os
import subprocess
import re
import urllib2
import time
base_path = '/y/data/whois'

for file in os.listdir(base_path):

    path = base_path +'/'  + file
    print path
    if not re.search("gz$", path):
        continue

    proc = subprocess.Popen(['gunzip','-c',path], stdout=subprocess.PIPE)

    for line in proc.stdout:
        #soup = BeautifulSoup(line)
        #line = soup.__str__("UTF-8")
        #line = unicode(soup)

        #print line
        #try:
        try:
            domain, scraper_internal_dns, scraper_ip, unixtime, whois_text, dig_text, failed  = line.split("\t") #line.split("") # ) "\t"
        except Exception, e:
            print "Couldn't parse: " + line
            print e
            continue


        if failed != '1':

            whois_text = urllib2.unquote(whois_text)

            print whois_text
            time.sleep (1)