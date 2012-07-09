from google.appengine.ext import db

class Paste(db.Model):
    name = db.StringProperty()
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
