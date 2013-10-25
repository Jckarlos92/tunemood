from google.appengine.ext import db

class User(db.Model):
    email = db.StringProperty(required = True)
    hash_pw = db.StringProperty(required = True)
    is_user = db.BooleanProperty(default = False)
    link_generated = db.StringProperty(required = True)

class Tag(db.Model):
    name = db.StringProperty(required = True)
