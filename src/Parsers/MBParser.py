# -*- coding: utf-8 -*-
'''
JobCrawler Monsterboard Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect
import logging

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
            try:
                beroep = soup.find('h1', {'class':'jobtitle'}).getText()
            except:
                beroep = ''
            try:
                opleiding = soup.find('span', {'itemprop':'educationRequirements'}).getText()
            except:
                opleiding = ''
            try:
                ervaring = soup.find('span', {'itemprop':'experienceRequirements'}).getText()
            except:
                ervaring = ''
            try:
                plaats = soup.find('div', {'class':'additionalinformation'}).find('span',{'class':'wrappable','itemprop':None}).getText()
            except:
                plaats = ''
            
            print 'Done parsing'
        
            logging.info("Inserted "+fullUrl)
            
            vacatureData = {'beroep':beroep,'plaats':plaats,'opleiding':opleiding,'jaren_werkervaring':ervaring}
            logging.info(vacatureData)
            
            self.db.insertVacature(vacatureData, fullUrl)