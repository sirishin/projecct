from flask import jsonify, request
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


def pro(i):
    print(i)
    sql = "SELECT * FROM datas WHERE id = \"%s\" " % i
    cursor, conn = db()
    cursor.execute(sql)
    all = cursor.fetchone()
    print(all)
    return {'number':all[0], 'id':all[1], 'name':all[3]}