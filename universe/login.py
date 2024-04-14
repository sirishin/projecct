from flask import request
import pymysql.cursors
import time

def db():
    conn = pymysql.connect(host='183.99.87.90',
            user='root',
            password='swhacademy!',
            db='Hee',
            charset='utf8')
    cursor = conn.cursor()
    return (cursor, conn)

def register():
    data = request.get_json()
    data = data['user']
    sql = "SELECT id, number FROM datas"
    cursor, conn = db()
    cursor.execute(sql)
    list_da = cursor.fetchall()
    cursor.close()
    conn.close()
    for a in list_da:
        if data['userid'] in a:
            return {'massege': 'fail', 'say': '이미 존재하는 아이디입니다.'}
        if int(data['number']) in a:
            return {'massege': 'fail', 'say': '이미 가입한 학번입니다.'}
        if len(data['number']) != 5:
            return {'massege': 'fail', 'say': '학번을 제대로 입력하여 주십시오.'}
        else:
            sql = "INSERT INTO datas (Number, id, password, name) VALUES ('%s', '%s' , '%s', '%s')" % (
            int(data['number']), data['userid'], data['password'], data['name'])
            cursor, conn = db()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return {'massege': 'seccess'}
    return data

def log():
    data = request.get_json()
    data = data['user']
    sql = "SELECT id, password FROM datas"
    cursor, conn = db()
    cursor.execute(sql)
    list_da = cursor.fetchall()
    cursor.close()
    conn.close()
    for a in list_da:
        if data['userid'] in a and data['password'] in a:
            return {'userid': data['userid'], 'password': data['password'], 'massege': 'seccess'}
    return {'messege': 'fail'}