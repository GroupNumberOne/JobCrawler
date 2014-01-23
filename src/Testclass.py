from Parsers.CVenVParser import CVenVParser
from bs4 import BeautifulSoup
import urllib2
import unittest

class TestParser(unittest.TestCase):
    def test_parser(self):
        cv = CVenVParser()
        url = 'http://cvenvacaturebank.nl/cv/110749/Technisch_Commercieel_Manager_Emmen.html'
        c=urllib2.urlopen(url)
        soup = BeautifulSoup(c, 'html5lib')
        
        data = cv.parseCV(soup, url)
        self.assertEqual(data,{'rijbewijs': True, 'woonplaats': u'Emmen', 'it_kennis': '', 'beroep': u'Technisch Commercieel Manager', 'jaren_werkervaring': 5, 'opleiding': u'HBO/ HTS'})

if __name__ == '__main__':
    unittest.main()