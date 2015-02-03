import datetime
from apps.main import db

class Srt(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    set_of_words = db.Column(db.Text())
    list_of_words = db.Column(db.Text())

class UpperWords(db.Model):
    word = db.Column(db.String(40), index = True, primary_key = True, unique = True)
    def __repr__(self):
        return self.word

class Phrases(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    phrase = db.Column(db.String(140), index = True)
    def __repr__(self):
        return str(self.phrase)
