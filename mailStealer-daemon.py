#!/usr/loca/bin/ python
import yaml
from datetime import datetime
import imaplib
import urllib
import re
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
from pymongo import Connection

c = pdc.Constants()
p = pdt.Calendar(c)

config = yaml.load(file('config.yaml', 'r'))
con = imaplib.IMAP4_SSL(config['imap_add'], config['imap_port'])
con.login(config['imap_email'], config['imap_pwd'])
con.select(config['imap_folder'])
typ, data = con.search(None, 'UNSEEN')
email_data = []
connection = Connection('localhost', 27017)
db = connection['muEmails']
for num in data[0].split():
    typ, e_data = con.fetch(num, '(RFC822)')
    r = re.compile('<br>', re.IGNORECASE)
    thisEmail = r.sub('\r\n', e_data[0][1])
    for n in thisEmail.split('\r\n'):
        email = ''
        date = ''
        client = ''
        subject = ''

        if n[:5] == 'From:':
            email = n.split(':')[1].strip()
        
        if n[:5] == 'Date:':
            print 'date: %s' % (n.replace('Date:', ''))
            date = p.parse(n.replace('Date:', '').strip())
        
        if n[:9] == 'X-Mailer:':
            client = n.split(':')[1].strip()
        
        if n[:5] == 'Subject:':
            subject = n.split(':')[1].strip()
            
    email_data.append({"email":email, "date":date,"client":client, "subject":subject}); 

db.insert(email_data);

con.close()
con.logout()
