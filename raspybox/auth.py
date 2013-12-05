'''
Modulo Authenticator
'''
from app import app, db
from flask_peewee.auth import Auth
from models import User


"Crea nuovo oggetto Authenticator"
auth = Auth(app, db, user_model=User)