'''
JobCrawler StarApple Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect

from DbHandler import DbHandler
    
class SAParser:    
        
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
        
    kennisArray = ['java ','java-','java/','java)','c++',re.escape('c#'),'javascript','.net','html','css','python','ruby','perl','mysql','oracle','postgresql','android','vmware','istqb','tmap']
    
    db = DbHandler()
    
    def findValues(self,soup,v,tag='span'):
        return soup.find(tag, id=v).text
    
    def findBeroep(self,soup):
        #find the second <h3> tag and take it's contents
        text = str(soup)
        x = str(soup).find('</h1>')
        text = text[x+4:]
        start = text.find('<h1>')
        end = text.find('</h1>')
        text = text[start+4:end]
        return text
        
    def findOmschrijving(self,soup):
        text = str(soup)[str(soup).find('<h3>Functie</h3>'):] #Take the html as a string to find the exact header
        start = text.find('<p>')
        end = text.find('</p>')
        text = text[start+3:end].split() #This is to lose excess space at either end of the string.
        text2 = ''
        for s in text:
            text2 = text2 + s + " "
        return text2
    
    def findOpleiding(self,soup):
        text = soup.find('div', id='inhoud').text
        text = str(text).lower()
        if text.find(' mbo ') != -1 or text.find('/mbo') != -1 or text.find('/mbo') != -1 or text.find('mbo-') != -1 or text.find('mbo+') != -1:
            return 'MBO'
        elif text.find(' havo ') != -1 or text.find('/havo') != -1 or text.find('/havo') != -1 or text.find('havo-') != -1 or text.find('havo+') != -1:
            return 'HAVO'
        elif text.find(' vwo ') != -1 or text.find('/vwo') != -1 or text.find('/vwo') != -1 or text.find('vwo-') != -1 or text.find('vwo+') != -1:
            return 'VWO'
        elif text.find(' hbo ') != -1 or text.find('hbo') != -1 or text.find('/hbo') != -1 or text.find('hbo-') != -1 or text.find('hbo+') != -1:
            return 'HBO'
        elif text.find(' wo ') != -1 or text.find('/wo') != -1 or text.find('/wo') != -1 or text.find('wo-') != -1 or text.find('wo+') != -1:
            return 'WO'
        else:
            return 'Test'
        
    def findKennis(self,soup):
        
        if str(soup).find('content="StarApple, Vacature') != -1:
            text = str(soup)[str(soup).find('<h3>Eisen</h3>'):] #Take the html as a string to find the exact header
            start = text.find('<p>')
            end = text.find('</p>')
            text = text[start+3:end].lower()
        else:
            text = str(soup)[str(soup).find('<h3>De kandidaat</h3>'):] #Take the html as a string to find the exact header
            start = text.find('<p>')
            end = text.find('</p>')
            text = text[start+3:end].lower()   
            
        kennis = ''
        
        length = len(text)
        x= 0
        
        while x <= length: # check wether a word of interest is at the current iteration
            for s in self.kennisArray:
                if (text[x:]).find(s) == 0 or (text[x:]).find(s) == 1:
                    if len(kennis) < 2:
                        kennis = s
                    else:
                        kennis = kennis + ', ' + s
            x = x + 2
            
        return kennis
    
    def parseCV(self,soup,fullUrl=None):
        
        beroep = self.findBeroep(soup)
        kennis = self.findKennis(soup)
        woonplaats = self.findValues(soup,'standplaats')
        woonplaats = woonplaats.split()[0]
        
        cvData = {'beroep':beroep, 'it_kennis': kennis, 'woonplaats':woonplaats}
        
        self.db.insertCV(cvData,fullUrl)
        
    def parseVacature(self,soup,fullUrl=None):
        
        opleiding = self.findOpleiding(soup)
        plaats = self.findValues(soup,'standplaats')
        kennis = self.findKennis(soup)
        omschrijving = self.findOmschrijving(soup)
        
        vacatureData = {'opleiding':opleiding,'plaats':plaats,'it_kennis':kennis,'omschrijving':omschrijving}
        
        self.db.insertVacature(vacatureData, fullUrl)
    
    