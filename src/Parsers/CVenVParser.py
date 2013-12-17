'''
JobCrawler CV en Vacaturebank Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect

from DbHandler import DbHandler
    
class CVenVParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    
    db = DbHandler()
            
    def findValues(self,soup,v,tag='span'):
        tag = soup.find(tag,text=re.compile('.*'+v+'.*'))
        return None if tag is None else tag.parent.find('div').text
    
    def parseCV(self,soup,fullUrl=None):
        if self.findValues(soup,'ICT/ Automatisering','div') is None: #Means we have someone with ICT experience
            return
        print 'Parsing...'
        
        beroep = self.findValues(soup,'Beroep')
        opleiding = self.findValues(soup,'Niveau')
        woonplaats = self.findValues(soup,'Woonplaats')
        provincie = self.findValues(soup,'Provincie')
        leeftijd = self.findValues(soup,'Leeftijd')
        if leeftijd != None:
            leeftijd = leeftijd.split()[0]
        
        if soup.find('span',text=re.compile('.*Rijbewijs.*')) >= 0:
            rijbewijs = (self.findValues(soup,'Rijbewijs').find('B') >= 0)
        else:
            rijbewijs = False    
            
        print 'Done parsing'
        
        cvData = {'beroep':beroep, 'opleiding': opleiding, 'woonplaats':woonplaats,'rijbewijs':rijbewijs}
        
        self.db.insertCV(cvData,fullUrl)
        
    def parseVacature(self,soup,fullUrl=None):
        if self.findValues(soup,'ICT/ Automatisering','div') is None: #ICT job
            return
        print 'Parsing...'
        
        beroep = self.findValues(soup,'Beroep')
        opleiding = self.findValues(soup,'Niveau')
        dienstverband = self.findValues(soup,'Dienstverband')
        plaats = self.findValues(soup,'Regio')
        kennis = self.findValues(soup,'Kennis')
        omschrijving = self.findValues(soup,'Functieomschrijving')
            
        print 'Done parsing'
        
        vacatureData = {'beroep':beroep,'opleiding':opleiding,'dienstverband':dienstverband,'plaats':plaats,'it_kennis':kennis,'omschrijving':omschrijving}
        
        self.db.insertVacature(vacatureData, fullUrl)