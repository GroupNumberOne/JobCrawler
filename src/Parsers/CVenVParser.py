# -*- coding: utf-8 -*-
'''
JobCrawler CV en Vacaturebank Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect
import urllib2

from DbHandler import DbHandler
    
class CVenVParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    kennisArray = ['apache','php','java','c++','c#','javascript','.net','html','css','python','ruby','perl','mysql','oracle','postgresql','android','vmware','istqb','tmap']
    
    db = DbHandler()
            
    def findValues(self,soup,v,tag='span'):
        tag = soup.find(tag,text=re.compile('.*'+v+'.*'))
        return None if tag is None else tag.parent.find('div').text
    
    def handleKennis(self,kennis):
        kennis_string = ''
        kennis = kennis.lower()
        for k in self.kennisArray:
            k=k.lower()
            if kennis.find(k) > 0:
                kennis_string += k+', '
                
        kennis_string = kennis_string.rstrip(', ')
        return kennis_string
                
    def handleExperience(self,soup):
        soup = soup.find('div', {'class':'detail'}).getText()
        start = soup.find('ICT/ Automatisering')
        end = soup.find(')',start)
        ervaring = [int(s) for s in list(soup[start:end+1]) if s.isdigit()]

        if len(ervaring) > 0:
            ervaring = ervaring[0]
        else:
            ervaring = None
            
        return ervaring
    
    def parseCV(self,soup,fullUrl=None):
        if self.findValues(soup,'ICT/ Automatisering','div') is None: #Means we have someone with ICT experience
            return
        try:
            jaren_werkervaring = self.handleExperience(soup)
        except:
            jaren_werkervaring = 0
        beroep = self.findValues(soup,'Beroep')
        opleiding = self.findValues(soup,'Niveau')
        woonplaats = self.findValues(soup,'Woonplaats')
        provincie = self.findValues(soup,'Provincie')
        leeftijd = self.findValues(soup,'Leeftijd')
        try:
            kennis = self.handleKennis(soup.find('div', {'class':'detail'}).getText())
        except:
            kennis = ''

        if leeftijd != None:
            leeftijd = leeftijd.split()[0]
        
        if soup.find('span',text=re.compile('.*Rijbewijs.*')) >= 0:
            rijbewijs = (self.findValues(soup,'Rijbewijs').find('B') >= 0)
        else:
            rijbewijs = False    
        
        cvData = {'beroep':beroep, 'opleiding': opleiding, 'woonplaats':woonplaats,'rijbewijs':rijbewijs, 'jaren_werkervaring':jaren_werkervaring,'it_kennis':kennis}
        
        self.db.insertCV(cvData,fullUrl)
        
    def parseVacature(self,soup,fullUrl=None):
        if self.findValues(soup,'ICT/ Automatisering','div') is None: #ICT job
            return
        
        beroep = self.findValues(soup,'Beroep')
        opleiding = self.findValues(soup,'Niveau')
        dienstverband = self.findValues(soup,'Dienstverband')
        plaats = self.findValues(soup,'Regio')
        try:
            kennis = self.handleKennis(self.findValues(soup,'Kennis'))
        except:
            kennis = ''
        omschrijving = self.findValues(soup,'Functieomschrijving')
        
        vacatureData = {'functie':beroep,'niveau':opleiding,'dienstverband':dienstverband,'plaats':plaats,'it_kennis':kennis,'omschrijving':omschrijving}
        
        self.db.insertVacature(vacatureData, fullUrl)