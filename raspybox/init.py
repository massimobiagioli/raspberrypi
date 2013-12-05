'''
Script di inizializzazione database
Va lanciato la prima volta, per creare l'utente admin che consente di accedere alla console
'''
from auth import auth

admin = auth.User(username='admin', admin=True, active=True)
admin.set_password('admin')
admin.email = 'admin@localhost.it'
admin.save()