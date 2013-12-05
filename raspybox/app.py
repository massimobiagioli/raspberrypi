'''
Modulo Applicazione
'''
from flask import Flask
from flask_peewee.db import Database


"Crea nuovo oggetto applicazione"
app = Flask(__name__)
app.config.from_object('config.Configuration')

"Crea nuovo oggetto per l'accesso al database sqlite"
db = Database(app)

"Inizializza moduli applicazione"
appModules = {}

def registerAppModule(moduleKey, instance):
    '''
    Registra modulo in applicazione
    @param moduleKey: Chiave del modulo da registrare
    @param instance: Istanza dell'oggetto di gestione del modulo  
    '''
    appModules[moduleKey] = instance    
    
def unregisterAppModule(moduleKey):
    '''
    De-registra modulo in applicazione
    @param moduleKey: Chiave del modulo da registrare  
    '''
    appModules.pop(moduleKey, None)