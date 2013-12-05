'''
Startup progetto
'''
from admin import admin
from api import api
from app import app, registerAppModule
from common import *
from models import *
from relayboard import RelayBoard
from routes import *
import os


"Imposta path di avvio progetto"
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

"Configura console di amministrazione e modulo per effettuare le chiamate Restful"
admin.setup()
api.setup()

def createTables():
    '''
    Crea tabelle
    '''
    User.create_table(fail_silently = True)
    Relay.create_table(fail_silently = True)

def initModules():
    '''
    Inizializza moduli applicazione
    '''
    registerAppModule(MODULE_RELAY_BOARD, RelayBoard())    

if __name__ == '__main__':
    createTables()
    initModules()
    app.run(host='0.0.0.0', port = 8080, debug = True)
