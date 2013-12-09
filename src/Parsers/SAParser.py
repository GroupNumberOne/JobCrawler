import psycopg2
from bs4 import BeautifulSoup
import re
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import DbHandler
    
def findValues(soup,v,tag='span'):
    tag = soup.find(tag,text=re.compile('.*'+v+'.*'))
    return None if tag is None else tag.parent.find('div').text

def parseCV(soup,fullUrl=None):
    print fullUrl
    '''
    
    if findValues(soup,"ICT/ Automatisering","div") is None: #Means we have someone with ICT experience
        return
    print "Parsing..."
    
    beroep = findValues(soup,"Beroep")
    opleiding = findValues(soup,"Niveau")
    woonplaats = findValues(soup,"Woonplaats")
    geslacht = findValues(soup,"Geslacht")
    provincie = findValues(soup,"Provincie")
    leeftijd = findValues(soup,"Leeftijd")
    if leeftijd != None:
        leeftijd = leeftijd.split()[0]
    
    if soup.find('span',text=re.compile('.*Rijbewijs.*')) >= 0:
        rijbewijs = (findValues(soup,"Rijbewijs").find('B') >= 0)
    else:
        rijbewijs = False
    
    cvData = {'beroep':beroep, 'opleiding': opleiding, 'woonplaats':woonplaats,'geslacht':geslacht,'provincie':provincie,'leeftijd':leeftijd,'rijbewijs':rijbewijs}
    
    DbHandler.insertCV(cvData,fullUrl)
    '''
def parseVacature(soup,fullUrl=None):
    print fullUrl
    '''
    if findValues(soup,"ICT/ Automatisering","div") is None: #ICT job
        return
    print "Parsing..."
    
    beroep = findValues(soup,"Beroep")
    opleiding = findValues(soup,"Niveau")
    dienstverband = findValues(soup,"Dienstverband")
    plaats = findValues(soup,"Regio")
    kennis = findValues(soup,"Kennis")
    omschrijving = findValues(soup,"Functieomschrijving")
    
    vacatureData = {'beroep':beroep,'opleiding':opleiding,'dienstverband':dienstverband,'plaats':plaats,'kennis':kennis,'omschrijving':omschrijving}
    
    DbHandler.insertVacature(vacatureData, fullUrl)
    '''