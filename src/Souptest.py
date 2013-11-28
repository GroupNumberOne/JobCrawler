from bs4 import BeautifulSoup
import urllib2

c=urllib2.urlopen('http://www.jobbird.com/nl/vacatures/124/techniek-industrie')
soup = BeautifulSoup(c, "lxml")
baseUrl = 'http://www.jobbird.com'
for a in soup.findAll('a'):
    if a.has_attr('href'):
        ref = a['href']
        if(ref.find('http') == 0):
            print a['href']
        elif(ref.find('/') == 0):
            print baseUrl+ref