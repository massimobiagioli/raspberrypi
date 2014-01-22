from cors import cross_origin
from flask import Flask, abort
from flask.globals import g, request
from flask.helpers import json
import hashlib
import hmac
import sqlite3

#Config
DATABASE = 'data/rpi-unit.db'
HOST = '127.0.0.1'
PORT = 3000
DEBUG = True

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

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

"""
@app.route('/listAll', methods=['OPTIONS', 'POST'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def show_entries():
    auth_token = request.headers.get('X-Auth')
    timestamp = request.headers.get('X-Timestamp')
    username = request.values.get('username')
    
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(username)        
"""

@app.route('/api/list/<tablekey>', methods=['OPTIONS', 'GET'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_list(tablekey):
    try:
        sql = 'SELECT * FROM ' + table_mapping[tablekey] + ' ORDER BY id'
        cursor = g.db.execute(sql)        
        "return json_response(cursor)"
        
        hash = hmac.new("segreta", "segreta", hashlib.sha256).hexdigest()
        
        "return json.dumps(request.headers['X-Auth'])"
        return json.dumps(hash)
    except:
        abort(500)

@app.route('/api/get/<tablekey>/<int:tableid>', methods=['OPTIONS', 'GET'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_get(tablekey, tableid):
    try:
        sql = 'SELECT * FROM ' + table_mapping[tablekey] + ' WHERE id=' + str(tableid)
        cursor = g.db.execute(sql)
        return json_response(cursor)
    except:
        abort(500)

@app.route('/api/insert/<tablekey>', methods=['OPTIONS', 'POST'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_insert(tablekey):
    try:
        columns = ', '.join(request.values.keys())
        placeholders = ', '.join('?' * len(request.values))        
        sql = 'INSERT INTO ' + table_mapping[tablekey] + ' ({}) VALUES ({})'.format(columns, placeholders)
        cursor = g.db.execute(sql, request.values.values())
        return json.dumps(str(cursor.lastrowid))        
    except:
        abort(500)

@app.route('/api/update/<tablekey>/<int:tableid>', methods=['OPTIONS', 'POST'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_update(tablekey, tableid):
    try:
        values = ', '.join('{}=?'.format(k) for k in request.values)       
        sql = 'UPDATE ' + table_mapping[tablekey] + ' SET {} WHERE id={}'.format(values, str(tableid))        
        g.db.execute(sql, request.values.values())
        return json.dumps(str(tableid))
    except:
        abort(500)

@app.route('/api/delete/<tablekey>/<int:tableid>', methods=['OPTIONS', 'DELETE'])
@cross_origin(headers=['X-Auth', 'X-Timestamp'])
def model_delete(tablekey, tableid):
    try:
        sql = 'DELETE FROM ' + table_mapping[tablekey] + ' WHERE id=' + str(tableid)
        g.db.execute(sql)
        return json.dumps(str(tableid))
    except:
        abort(500)
    
if __name__ == '__main__':    
    app.run(app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
