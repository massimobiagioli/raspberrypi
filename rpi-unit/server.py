from cors import cross_origin
from crypt import xor_decrypt
from flask import Flask
from flask.globals import g, request
from flask.wrappers import Response
import hashlib
import hmac
import json
import sqlite3


#Config
DATABASE = 'data/rpi-unit.db'
HOST = '127.0.0.1'
PORT = 3000
DEBUG = False

#Const
CRYPT_KEY = 'Qwerty456$%&'
ERR_MSG_401 = 'Unauthorized';
ERR_MSG_500 = 'Internal Server Error';

#Database Mapping
table_mapping = {}
table_mapping['user'] = 'users'
table_mapping['device_type'] = 'device_types'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'], isolation_level=None)

def json_response(cursor):
    return json.dumps([dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()])

def check_aut(request):
    try:        
        password = read_user_password(request.headers['X-Username'])
        auth_token = request.headers['X-Auth']     
        username = request.headers['X-Username']   
        timestamp = request.headers['X-Timestamp']
        salted = password + hmac.new(username + password + timestamp, timestamp, hashlib.sha256).hexdigest()              
        calc_hash = hmac.new(salted, password + username + timestamp + salted, hashlib.sha256).hexdigest()
        return calc_hash == auth_token 
    except:
        return False

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

def read_user_password(username):            
    sql = "SELECT password FROM users WHERE username='%s'" % username 
    cursor = g.db.execute(sql)        
    row = cursor.fetchone()
    return xor_decrypt(row[0].encode('ascii', 'ignore'), CRYPT_KEY)

@app.route('/api/list/<tablekey>', methods=['OPTIONS', 'GET'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_list(tablekey):
    try:                                               
        if check_aut(request):
            sql = 'SELECT * FROM ' + table_mapping[tablekey] + ' ORDER BY id'
            cursor = g.db.execute(sql)        
            return json_response(cursor)
        else:
            return Response(ERR_MSG_401, 401)
    except:
        return Response(ERR_MSG_500, 500)

@app.route('/api/get/<tablekey>/<int:tableid>', methods=['OPTIONS', 'GET'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_get(tablekey, tableid):
    try:
        if check_aut(request):
            sql = 'SELECT * FROM ' + table_mapping[tablekey] + ' WHERE id=' + str(tableid)
            cursor = g.db.execute(sql)
            return json_response(cursor)
        else:
            return Response(ERR_MSG_401, 401)
    except:
        return Response(ERR_MSG_500, 500)

@app.route('/api/insert/<tablekey>', methods=['OPTIONS', 'POST'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_insert(tablekey):
    try:
        if check_aut(request):
            columns = ', '.join(request.values.keys())
            placeholders = ', '.join('?' * len(request.values))        
            sql = 'INSERT INTO ' + table_mapping[tablekey] + ' ({}) VALUES ({})'.format(columns, placeholders)
            cursor = g.db.execute(sql, request.values.values())
            return json.dumps(str(cursor.lastrowid))
        else:
            return Response(ERR_MSG_401, 401)        
    except:
        return Response(ERR_MSG_500, 500)

@app.route('/api/update/<tablekey>/<int:tableid>', methods=['OPTIONS', 'POST'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_update(tablekey, tableid):
    try:
        if check_aut(request):
            values = ', '.join('{}=?'.format(k) for k in request.values)       
            sql = 'UPDATE ' + table_mapping[tablekey] + ' SET {} WHERE id={}'.format(values, str(tableid))        
            g.db.execute(sql, request.values.values())
            return json.dumps(str(tableid))
        else:
            return Response(ERR_MSG_401, 401)   
    except:
        return Response(ERR_MSG_500, 500)

@app.route('/api/delete/<tablekey>/<int:tableid>', methods=['OPTIONS', 'DELETE'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_delete(tablekey, tableid):
    try:
        if check_aut(request):
            sql = 'DELETE FROM ' + table_mapping[tablekey] + ' WHERE id=' + str(tableid)
            g.db.execute(sql)
            return json.dumps(str(tableid))
        else:
            return Response(ERR_MSG_401, 401)
    except:
        return Response(ERR_MSG_500, 500)
    
if __name__ == '__main__':    
    app.run(app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
    
