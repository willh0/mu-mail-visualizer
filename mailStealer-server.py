import web
import json
from datetime import datetime
from datetime import date
from pymongo import Connection
from dateutil import parser

urls = (
    '/count/(.*)', 'count',
    '/daycount/(.*)', 'dayCount',
    '/type/(.*)', 'type'
)
app = web.application(urls, globals())

class dayCount:        
    def GET(self, ts):
        web.header('Content-Type', 'application/javascript')
        connection = Connection('localhost', 27017)
        db = connection['emailDb']
        collection = db['muEmails']
        d = datetime.utcfromtimestamp(int(ts) / 1000)
        now = collection.find({"date": {"$gt": d}})
        callback = web.ctx.query.split("&")[0].split("=")[1]
        return callback + "("+ json.dumps({"count": now.count()}) + ")" 

class count:        
    def GET(self, ts):
        web.header('Content-Type', 'application/javascript')
        connection = Connection('localhost', 27017)
        db = connection['emailDb']
        collection = db['muEmails']
        d = datetime.utcfromtimestamp(int(ts) / 1000)
        print "\nDate: %s\n" % (d)
        print "\nNow: %s\n" % (datetime.utcnow())
        now = collection.find({"date": {"$gt": d}})
        callback = web.ctx.query.split("&")[0].split("=")[1]
        return callback + "("+ json.dumps({"count": now.count()}) + ")" 

class type:        
    def GET(self, ts):
        web.header('Content-Type', 'application/javascript')
        connection = Connection('localhost', 27017)
        db = connection['emailDb']
        collection = db['muEmails']
        callback = web.ctx.query.split("&")[0].split("=")[1]
        if (ts):
            d = datetime.utcfromtimestamp(int(ts) / 1000)
            things = collection.find({"date": {"$gt": d}})
            things = collection.find()
        else:
            things = collection.find()
            
        data = { 'reply':0, 'unsub':0, 'dues':0, 'login':0, 'tools':0, 'start':0, 'churn':0, 'find':0, 'mship':0, 'comm':0, 'spam':0, 'bug':0, 'abuse':0, 'gross':0, 'copy':0, 'other':0, 'angry':0 }

        for thing in things:
            if not thing['subject']:
                break;
            elif thing['subject'].strip() == "Submitted from site: Organizer Dues / Billing Issues":
                data['dues'] += 1
            elif thing['subject'].strip() == "Submitted from site: Login / Password Issues":
                data['login'] += 1
            elif thing['subject'].strip() == "Submitted from site: Organizer: Tools and Settings":
                data['tools'] += 1
            elif thing['subject'].strip() == "Submitted from site: Organizer: Starting a Group":
                data['start'] += 1
            elif thing['subject'].strip() == "Submitted from site: Organizer: Step down from Group":
                data['churn'] += 1
            elif thing['subject'].strip() == "Submitted from site: Member: Finding / Joining Groups":
                data['find'] += 1
            elif thing['subject'].strip() == "Submitted from site: Member: Managing Memberships":
                data['mship'] += 1
            elif thing['subject'].strip() == "Submitted from site: Communications & Group email settings":
                data['comm'] += 1
            elif thing['subject'].strip() == "Submitted from site: Report Spam / Inappropriate Content":
                data['spam'] += 1
            elif thing['subject'].strip() == "Submitted from site: Report Bug":
                data['bug'] += 1
            elif thing['subject'].strip() == "Submitted from site: Report Member Abuse":
                data['abuse'] += 1
            elif thing['subject'].strip() == "Submitted from site: Report Inappropriate Meetup Group":
                data['gross'] += 1
            elif thing['subject'].strip() == "Submitted from site: Report Copyright / Trademark Issue":
                data['copy'] += 1
            elif thing['subject'].strip() == "Submitted from site: Unsubscribe / Delete Account":
                data['unsub'] += 1
            elif thing['subject'].strip().upper() == thing['subject'].strip():
                data['angry'] += 1
            elif thing['subject'].strip() == "Submitted from site: Other":
                data['other'] += 1
            elif thing['subject'].strip().lower()[:3] == "re:":
                data['reply'] += 1

            if thing['subject'].strip().lower() == "unsubscribe":
                data['unsub'] += 1

        return callback + "("+json.dumps(data) + ")" 

if __name__ == "__main__":
    app.run()
