#!/usr/loca/bin/ python
import yaml
from datetime import datetime
import imaplib
import dateutil.parser
import urllib
import pymongo

config = yaml.load(file('config.yaml', 'r'))
con = imaplib.IMAP4_SSL(config['imap_add'], config['imap_port'])
con.login(config['imap_email'], config['imap_pwd'])
con.select(config['imap_folder'])
typ, data = con.search(None, 'UNSEEN')
data = []
connection = Connection('localhost', 27017)
db = connection['muEmails']
for num in data[0].split():
    typ, data = con.fetch(num, '(RFC822)')
    for n in data[0][1].split('\r\n'):
        if n[:5] == 'From:':
            email = n.split(':')[1].strip()
        
        if n[:5] == 'Date:':
            date = dateutil.parser.parse(n.split(':')[1].strip())
        
        if n[:9] == 'X-Mailer:':
            client = n.split(':')[1].strip()
        
        if n[:5] == 'Subject:':
            subject = n.split(':')[1].strip()
            
        data.append({"email":email, "date":date,"client":client, "subject":subject}); 

db.insert(data);

con.close()
con.logout()
