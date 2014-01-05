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
import urllib2

from DbHandler import DbHandler

class MBParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    
    kennisArray = ['apache','php','uml','java','c++','c#','javascript','.net','html','css','python','ruby','perl','mysql','oracle','postgresql','android','vmware','istqb','tmap']
        
    db = DbHandler()    
        
    def findValues(self,soup,v,tag='span'):
        tag = soup.find(tag,text=re.compile('.*'+v+'.*'))
        return None if tag is None else tag.parent.find('div').text
    
    def handleKennis(self,kennis):
        kennis_string = ''
        kennis = kennis.lower()
        for k in self.kennisArray:
            k = k.lower()
            if kennis.find(k) > 0:
                kennis_string += k+', '
                
        kennis_string = kennis_string.rstrip(', ')
        return kennis_string
        
    def parseVacature(self,soup,fullUrl=None):
        if soup.find('div', {'class':'additionalinformation'}) is None and soup.find('div', {'id':'jobsummary'}) is None:
            return
        
        if soup.find('div', {'class':'additionalinformation'}) is not None and soup.find('span', {'itemprop':'occupationalCategory'}).getText() == 'IT / Software Development':
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
                ervaring = [int(s) for s in ervaring.split() if s.isdigit()]
                ervaring = ervaring[0]
            except:
                ervaring = ''
            try:
                plaats = soup.find('div', {'class':'additionalinformation'}).find('span',{'class':'wrappable','itemprop':None}).getText()
            except:
                plaats = ''
            try:
                it_kennis = self.handleKennis(soup.find('div',{'itemprop':'description'}).getText())
            except:
                it_kennis = ''
            
            vacatureData = {'functie':beroep,'plaats':plaats,'opleiding':opleiding,'jaren_werkervaring':ervaring,'it_kennis':it_kennis}
            
            self.db.insertVacature(vacatureData, fullUrl)
            
        elif soup.find('div', {'id':'jobsummary'}) is not None and (soup.find('div', {'id':'jobsummary'}).getText().find("IT - software") > 0 or soup.find('div', {'id':'jobsummary'}).getText().find("IT - internet") > 0):
            try:
                beroep = soup.find('h1', {'itemprop':'title'}).getText()
            except:
                beroep = ''
            try:
                opleiding = soup.find('span', {'itemprop':'educationRequirements'}).getText()
            except:
                opleiding = ''
            try:
                ervaring = soup.find('span', {'itemprop':'experienceRequirements'}).getText()
                ervaring = [int(s) for s in ervaring.split() if s.isdigit()]
                ervaring = ervaring[0]
            except:
                ervaring = ''
            try:
                plaats = soup.find('div', {'id':'jobsummary'}).find('span',{'class':'wrappable','itemprop':'jobLocation'}).getText()
                plaats = plaats.split(',')[0]
            except:
                plaats = ''
            try:
                it_kennis = self.handleKennis(soup.find('div',{'itemprop':'description'}).getText())
            except:
                it_kennis = ''
            
            vacatureData = {'functie':beroep,'plaats':plaats,'opleiding':opleiding,'jaren_werkervaring':ervaring,'it_kennis':it_kennis}
            
            self.db.insertVacature(vacatureData, fullUrl)