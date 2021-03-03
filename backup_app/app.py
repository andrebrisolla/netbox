import threading
import asyncio
import time
from flask import Flask,request
from backup import Backup


def run_backup():
    while True:
        # Execute backup
        Backup().create_backup()
        time.sleep(86400)

app = Flask(__name__)
app.run()

@app.route('/backup_app/login',methods=['POST','GET'])
def login():
    data = request.form
    return Backup().login(data)

@app.route('/backup_app/login/check',methods=['POST','GET'])
def login_check():
    
    data = request.form
    return Backup().login_check(data)

@app.route('/backup_app/backup/create',methods=['POST','GET'])
def backup_create():
    
    data = request.form
    
    check_login = Backup().login_check(data)
    if check_login['code'] == 200:
        return Backup().create_backup()
    else:
        return {
            'code' : 403,
            'message' : "Acesso negado!"
        }

@app.route('/backup_app/backup/list',methods=['POST','GET'])
def backup_list():
    data = request.form
    
    check_login = Backup().login_check(data)
    if check_login['code'] == 200:
        return Backup().backup_list()
    else:
        return {
            'code' : 403,
            'message' : "Acesso negado!"
        }

@app.route('/backup_app/backup/remove',methods=['POST','GET'])
def backup_delete():
    data = request.form
    return Backup().backup_delete(data)
    
@app.route('/backup_app/backup/restore',methods=['POST','GET'])
def backup_restore():
    data = request.form
    return Backup().backup_restore(data)

# Start thread
t=threading.Thread(target=run_backup)
t.start()

