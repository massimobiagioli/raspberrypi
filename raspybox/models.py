'''
Modelli
'''
from app import db
from flask_peewee.auth import BaseUser
from peewee import *
import datetime


class User(db.Model, BaseUser):
    '''
    Utente
    '''
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username


class Relay(db.Model):
    '''
    Relay
    '''
    channel = IntegerField()
    device = CharField()
    active = BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.channel) + ":" + self.device        