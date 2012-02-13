#!/usr/loca/bin/ python
import yaml
from datetime import datetime
import imaplib
import urllib
import re
from pymongo import Connection

config = yaml.load(file('/Users/whoward/mu-mail-visualizer/mu-mail-visualizer/config.yaml', 'r'))
con = imaplib.IMAP4_SSL(config['imap_add'], config['imap_port'])
con.login(config['imap_email'], config['imap_pwd'])
con.select(config['imap_folder'])
typ, data = con.search(None, 'UNSEEN')
email_data = []
connection = Connection('localhost', 27017)
db = connection['emailDb']
collection = db['muEmails']
for num in data[0].split():
    typ, e_data = con.fetch(num, '(RFC822)')
    r = re.compile('<br>', re.IGNORECASE)
    thisEmail = r.sub('\r\n', e_data[0][1])
    email = ''
    myDate = ''
    client = ''
    subject = ''
    for n in thisEmail.split('\r\n'):

        if n[:9] == 'X-Mailer:':
            client = n.replace('X-Mailer:', '').strip()
        
        if n[:8] == 'Subject:':
            subject = n.replace('Subject:', '').strip()

    if subject != '':
        email_data.append({'date':datetime.utcnow(), 'client':client, 'subject':subject}); 

print email_data

if len(email_data) > 0:
    collection.insert(email_data);

con.close()
con.logout()
