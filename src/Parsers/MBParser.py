'''
JobCrawler Monsterboard Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect

from DbHandler import DbHandler

class MBParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
        
    db = DbHandler()    
        
    def findValues(self,soup,v,tag='span'):
        tag = soup.find(tag,text=re.compile('.*'+v+'.*'))
        return None if tag is None else tag.parent.find('div').text
        
    def parseVacature(self,soup,fullUrl=None):
        if soup.find('div', {'class':'additionalinformation'}) is None:
            return
        print 'Parsing...'
        if soup.find('span', {'itemprop':'occupationalCategory'}).getText() == 'IT / Software Development' and soup.find('div', {'class':'additionalinformation'}) is not None:
            beroep = soup.find('h1', {'class':'jobtitle'}).getText()
            opleiding = soup.find('span', {'itemprop':'educationRequirements'}).getText()
            ervaring = soup.find('span', {'itemprop':'experienceRequirements'}).getText()
            plaats = soup.find('div', {'class':'additionalinformation'}).find('span',{'class':'wrappable','itemprop':None}).getText()
            
            print 'Done parsing'
        
            
            vacatureData = {'beroep':beroep,'plaats':plaats,'opleiding':opleiding,'jaren_werkervaring':ervaring}
            print vacatureData
            
        self.db.insertVacature(vacatureData, fullUrl)