'''
Isolated SQL statements
'''
date_sql = """UPDATE {0} SET lastcrawled = current_date WHERE fullUrl = '{1}'"""

gurl_sql = """SELECT fullurl from {0} WHERE baseurl LIKE '%{1}%' AND fullurl LIKE '%{2}%' AND (lastcrawled <= current_date - integer '0' OR lastcrawled IS NULL)
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
            (it_kennis,eisen,plaats,bedrijfsnaam,functie,uren,salaris,niveau,omschrijving,kennis,dienstverband)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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