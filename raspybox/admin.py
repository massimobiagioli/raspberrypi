'''
Modulo di Amministrazione
Accesso all'area admin: http://localhost:8080/admin
'''
from app import app
from auth import auth
from flask_peewee.admin import Admin, ModelAdmin
from models import Relay


class RelayAdmin(ModelAdmin):
    '''
    Amministrazione Model Relay
    '''
    columns = ('channel', 'device', 'active',)

"Crea oggetto Admin associandolo ad un'Authenticator"
admin = Admin(app, auth)
auth.register_admin(admin)

"Registra Model"
admin.register(Relay, RelayAdmin)