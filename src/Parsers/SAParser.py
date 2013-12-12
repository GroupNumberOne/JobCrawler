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

#import DbHandler
    
def findValues(soup,v,tag='span',case=0):
    if case == 0:
        return soup.find(tag, id=v).text
    if case == 1:
        #als het voor de omschrijving is moet de inhoud gepakt worden en daarbinnen de 1e of 2e header
        return

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
    
    #zoek naar sleutelwoorden
    #beroep = findValues(soup,"Beroep")
    #zoek naar sleutelwoorden
    #opleiding = findValues(soup,"Niveau")
    plaats = findValues(soup,'standplaats')
    #zoek naar sleutelwoorden
    #kennis = findValues(soup,"Kennis")
    omschrijving = findValues(soup,'inhoud','div')
    print omschrijving
    uren = int(findValues(soup, 'uren').split()[0])
    try:
        salarisTxt = findValues(soup,'inhoud','div')
        #vind euroteken in de tekst en sla het bedrag erna op in salaris
        #salarisTxt = salarisTxt[salarisTxt.find('&euro;'),salarisTxt.find('&euro;')+7]
        salaris = int(salarisTxt.split()[1])
        print salaris
    except:
        salaris = 0;
    
    vacatureData = {'plaats':plaats,'omschrijving':omschrijving, 'uren':uren, 'salaris':salaris}
    print vacatureData
    #DbHandler.insertVacature(vacatureData, fullUrl)