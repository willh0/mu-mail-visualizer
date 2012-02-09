#!/usr/loca/bin/ python
import yaml
from datetime import datetime
import imaplib
import urllib

config = yaml.load(file(config.yaml, 'r'))
con = imaplib.IMAP4_SSL(config['imap_add'], config['imap_port'])
con.login(config['imap_email'], config['imap_pwd'])
con.select(config['imap_folder'])
typ, data = con.search(None, 'UNSEEN')
for num in data[0].split():
    print num;

con.close()
con.logout()
