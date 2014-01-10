'''
Isolated SQL statements
'''
date_sql = """UPDATE {0} SET lastcrawled = current_date,error=%s WHERE fullUrl = %s"""

gurl_sql = """SELECT fullurl from {0} WHERE baseurl LIKE '%{1}%' AND fullurl LIKE '%{2}%' AND (lastcrawled <= current_date - integer '5' OR lastcrawled IS NULL)
        ORDER BY lastcrawled ASC NULLS FIRST LIMIT {3}"""
        
url_sql = """INSERT INTO {0}
            (baseurl, fullurl)
            SELECT %s, %s
            WHERE
            NOT EXISTS (
            SELECT fullurl FROM {0} WHERE fullurl = %s
            );"""
            
vacature_sql = """ UPDATE {0} SET it_kennis=%s,eisen=%s,plaats=%s,bedrijfsnaam=%s,functie=%s,uren=%s,salaris=%s,niveau=%s,omschrijving=%s,kennis=%s,dienstverband=%s WHERE url=%s;
            INSERT INTO {0}
            (it_kennis,eisen,plaats,bedrijfsnaam,functie,uren,salaris,niveau,omschrijving,kennis,dienstverband,url)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE
            NOT EXISTS (
            SELECT url FROM {0} WHERE url = %s
            );"""
            
cv_sql = """ UPDATE {0} SET voornaam=%s,achternaam=%s,tussenvoegsels=%s,opleiding=%s,jaren_werkervaring=%s,woonplaats=%s,cursussen=%s,it_kennis=%s,rijbewijs=%s,beroep=%s WHERE url=%s;
            INSERT INTO {0}
            (voornaam,achternaam,tussenvoegsels,opleiding,jaren_werkervaring,woonplaats,cursussen,it_kennis,rijbewijs,beroep,url)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE
            NOT EXISTS (
            SELECT url FROM {0} WHERE url = %s
            );"""

crawlstate_sql = """ SELECT crawling,amount from crawlerstate WHERE site = %s """

crawlstate_all_sql = """ SELECT site,crawling,amount from crawlerstate ORDER BY id """

crawlstate_change_single = """ UPDATE crawlerstate SET crawling=%s,amount=%s WHERE site=%s"""

geocode_insert = """ INSERT INTO geocodes (city,latitude,longitude) VALUES (%s,%s,%s) """

geocode_get = """ SELECT count(city) FROM geocodes WHERE city=%s"""