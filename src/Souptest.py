from bs4 import BeautifulSoup
import urllib2

c=urllib2.urlopen('http://gaanders.home.xs4all.nl/pages/cv.html')
soup = BeautifulSoup(c, "lxml")
result = soup.find('div', {'id':'personaliarechts'})
print result.find('p').text