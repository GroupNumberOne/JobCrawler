'''
JobCrawler StarApple Parser class
Takes the useful information out of the page's HTML
and stores it in the Database
'''

import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import DbHandler
    
def findValues(soup,v,tag='span'):
    return soup.find(tag, id=v).text

def findBeroep(soup):
    #find the second <h3> tag and take it's contents
    text = str(soup)
    x = str(soup).find('</h1>')
    text = text[x+4:]
    start = text.find('<h1>')
    end = text.find('</h1>')
    text = text[start+4:end]
    return text
    
def findOmschrijving(soup):
    text = str(soup)[str(soup).find('<h3>Functie</h3>'):] #Take the html as a string to find the exact header
    start = text.find('<p>')
    end = text.find('</p>')
    text = text[start+3:end].split() #This is to lose excess space at either end of the string.
    text2 = ''
    for s in text:
        text2 = text2 + s + " "
    return text2

def findOpleiding(soup):
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
    
def findKennis(soup):
    
    kennisArray = ['java ','java-','java/','java)','c++',re.escape('c#'),'javascript','.net','html','css','python','ruby','perl','mysql','oracle','postgresql','android','vmware','istqb','tmap']

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
        for s in kennisArray:
            if (text[x:]).find(s) == 0 or (text[x:]).find(s) == 1:
                if len(kennis) < 2:
                    kennis = s
                else:
                    kennis = kennis + ", " + s
        x = x + 2
        
    return kennis

def parseCV(soup,fullUrl=None):
    print "Parsing..."
    
    beroep = findBeroep(soup)
    kennis = findKennis(soup)
    woonplaats = findValues(soup,'standplaats')
    woonplaats = woonplaats.split()[0]
    

    print kennis  
    print "Done parsing"
    
    cvData = {'beroep':beroep, 'opleiding': kennis, 'woonplaats':woonplaats}
    
    DbHandler.insertCV(cvData,fullUrl)
    
def parseVacature(soup,fullUrl=None):
    print "Parsing..."
    
    #beroep = findValues(soup,"Beroep")
    opleiding = findOpleiding(soup)
    plaats = findValues(soup,'standplaats')
    kennis = findKennis(soup)
    omschrijving = findOmschrijving(soup)
    #uren = int(findValues(soup, 'uren').split()[0])
    print kennis
    print "Done parsing"
    vacatureData = {'opleiding':opleiding,'plaats':plaats,'kennis':kennis,'omschrijving':omschrijving}
    
    DbHandler.insertVacature(vacatureData, fullUrl)
    
    