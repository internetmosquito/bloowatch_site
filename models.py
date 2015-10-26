__author__ = 'mosquito'
import datetime

from bloowatch import db


class RegisteredMail(db.Model):

    __tablename__ = "registered_users"

    email = db.Column(db.String, primary_key=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __init__(self, email, creation_time):
        self.email = email
        self.creation_date = creation_time

    def __repr__(self):
        return '<email {0}>'.format(self.email)


