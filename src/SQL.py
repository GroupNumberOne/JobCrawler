'''
Isolated SQL statements
'''
date_sql = """UPDATE %s SET lastcrawled = current_date WHERE fullUrl = '%s'"""

gurl_sql = """SELECT * from %s WHERE baseurl LIKE '%%s%' AND fullurl LIKE '%%s%' AND (lastcrawled <= current_date - integer '0' OR lastcrawled IS NULL)
        ORDER BY lastcrawled ASC NULLS FIRST LIMIT %s"""
        
url_sql = """INSERT INTO %s
            (baseurl, fullurl)
            SELECT %s, %s
            WHERE
            NOT EXISTS (
            SELECT fullurl FROM urls WHERE fullurl = %s
            );"""
            
vacature_sql = """ UPDATE %s SET it_kennis=%s,eisen=%s,plaats=%s,bedrijfsnaam=%s,functie=%s,uren=%s,salaris=%s,niveau=%s,omschrijving=%s,kennis=%s,dienstverband=%s WHERE url=%s;
            INSERT INTO %s
            (it_kennis,eisen,plaats,bedrijfsnaam,functie,uren,salaris,niveau,omschrijving,kennis,dienstverband)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE
            NOT EXISTS (
            SELECT url FROM %s WHERE url = %s
            );"""
            
cv_sql = """ UPDATE %s SET voornaam=%s,achternaam=%s,tussenvoegsels=%s,opleiding=%s,jaren_werkervaring=%s,woonplaats=%s,cursussen=%s,it_kennis=%s,rijbewijs=%s,bedroep=%s WHERE url=%s;
            INSERT INTO %s
            (voornaam,achternaam,tussenvoegsels,opleiding,jaren_werkervaring,woonplaats,cursussen,it_kennis,rijbewijs,bedroep)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE
            NOT EXISTS (
            SELECT url FROM %s WHERE url = %s
            );"""