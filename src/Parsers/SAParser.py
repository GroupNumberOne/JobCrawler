# -*- coding: utf-8 -*-
'''
JobCrawler StarApple Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect

#from DbHandler import DbHandler
    
class SAParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
            
    #db = DbHandler()
    
    def findValues(self,soup,v,tag='span'):
        return soup.find(tag, itemprop=v).getText()
    
    def findBeroep(self,soup):
        text = str(soup)
        x = text.find('"candidate-specifics"')
        text = text[x:]
        start = text.find('<h1>')
        end = text.find('</h1>')
        text = text[start+4:end]
        return text
    
    def findPlaats(self,soup):
        text = str(soup)
        x = text.find('<p class="subtitle">')
        text = text[x:]
        if text.find('<em>') >= 0:
            start = text.find('<em>')
            end = text.find('</em>')
            text = text[start+4:end]
            text = text.lower()
        else:
            text = ''
        return text
    
    def findOpleiding(self,soup):
        text = str(soup).lower()
        if text.find(' mbo ') != -1 or text.find('mbo/') != -1 or text.find('/mbo') != -1 or text.find('mbo-') != -1 or text.find('(mbo)') != -1  or text.find('mbo+') != -1:
            return 'MBO'
        elif text.find(' havo ') != -1 or text.find('havo/') != -1 or text.find('/havo') != -1 or text.find('havo-') != -1 or text.find('(havo)') != -1  or text.find('havo+') != -1:
            return 'HAVO'
        elif text.find(' vwo ') != -1 or text.find('vwo/') != -1 or text.find('/vwo') != -1 or text.find('vwo-') != -1 or text.find('(vwo)') != -1  or text.find('vwo+') != -1:
            return 'VWO'
        elif text.find(' hbo ') != -1 or text.find('hbo/') != -1 or text.find('/hbo') != -1 or text.find('hbo-') != -1 or text.find('(hbo)') != -1  or text.find('hbo+') != -1:
            return 'HBO'
        elif text.find(' wo ') != -1 or text.find('wo/') != -1 or text.find('/wo') != -1 or text.find('wo-') != -1 or text.find('(wo)') != -1  or text.find('wo+') != -1:
            return 'WO'
        else:
            return ''
        
    def findKennis(self,soup):
        kennis = ''
        text = str(soup)
        start = text.find('var graphData =')
        end = text[start:].find(';')
        text = text[start:start+end]
        while text.find('"skill":{"name"') != -1:
            text = text[text.find('"skill":{"name"'):]
            start = text.find(':"')
            end = text.find('"}')
            kennis = kennis + text[start+2:end].lower() + ","
            text = text[end:]
            
        return kennis
    
    
    def parseCV(self,soup,fullUrl=None):
        
        try:
            beroep = self.findBeroep(soup)
        except:
            beroep = ''
        try:
            kennis = self.findKennis(soup)
        except:
            kennis = ''
        try:
            woonplaats = self.findPlaats(soup)
        except:
            woonplaats = ''
        try:
            opleiding = self.findOpleiding(soup)
        except:
            opleiding = ''
        
        cvData = {'beroep':beroep, 'it_kennis': kennis, 'woonplaats':woonplaats,'opleiding':opleiding}
        
        self.db.insertCV(cvData,fullUrl)
        
    def parseVacature(self,soup,fullUrl=None):
        
        try:
            functie = self.findValues(soup,'title','h1')
        except:
            functie = ''
        try:
            opleiding = self.findOpleiding(soup)
        except:
            opleiding = ''
        try:
            plaats = self.findValues(soup,'addressLocality')
        except:
            plaats = ''
        try:
            kennis = self.findKennis(soup)
        except:
            kennis = ''
        try:
            omschrijving = self.findValues(soup,'responsibilities','p')
        except:
            omschrijving = ''
        try:
            uren = self.findValues(soup,'workHours','td')
            uren = int(uren[uren.find(',')-2:uren.find(',')])
        except:
            uren = None
        try:
            salaris = int(self.findValues(soup,'baseSalary'))
        except:
            salaris = None
        
        vacatureData = {'functie':functie,'niveau':opleiding,'plaats':plaats,'it_kennis':kennis,'omschrijving':omschrijving,'uren':uren,'salaris':salaris}
        
        self.db.insertVacature(vacatureData, fullUrl)
    
    