class Configuration(object):
    '''
    Classe configurazioni generali applicazione
    Contiene i parametri per la connessione al database e altre impostazioni generali
    '''
    DATABASE = {
        'name': 'data/raspybox.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }
    DEBUG = True
    SECRET_KEY = 'qwertyuiop'
