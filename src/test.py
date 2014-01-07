import urllib2
from bs4 import BeautifulSoup
from Parsers.SAParser import SAParser

feed = 'http://www.starapple.nl/werkgever/profielen/332/'

c=urllib2.urlopen(feed)
soup = BeautifulSoup(c, 'html5lib')
loweredfeed = feed.lower()

SAParser().parseCV(soup,feed)
