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
    print "Parsing..."
    
    #beroep = findValues(soup,"Beroep")
    #opleiding = findValues(soup,"Niveau")
    #dienstverband = findValues(soup,"Dienstverband")
    plaats = findValues(soup,"standplaats")
    #kennis = findValues(soup,"Kennis")
    omschrijving = findValues(soup,"inhoud","div")
    print omschrijving
    uren = int(findValues(soup, "uren").split()[0])
    
    vacatureData = {'plaats':plaats,'omschrijving':omschrijving, 'uren':uren}
    print vacatureData
    #DbHandler.insertVacature(vacatureData, fullUrl)