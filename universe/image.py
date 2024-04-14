import json

import pymysql.cursors
from flask import jsonify,request
import time
import base64
import requests


def db():
    conn = pymysql.connect(host='183.99.87.90',
            user='root',
            password='swhacademy!',
            db='Hee',
            charset='utf8')
    cursor = conn.cursor()
    return (cursor, conn)

def start():
    sql = "SELECT * from photobook"
    cursor, conn = db()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    sql = "SELECT num, title, ID, view, content, tiem, photo FROM photobook ORDER BY num desc"
    cursor.execute(sql)
    list_data = cursor.fetchall()
    text_list = []
    for obj in list_data:
        sql2 = "SELECT coment, num FROM comentsb WHERE num = %s" % obj[0]
        cursor.execute(sql2)
        coments = cursor.fetchall()
        c = []
        get_image = obj[6]
        # print(get_image)
        get_image = get_image.decode('utf-8')
        for a in coments:
            c.append(a[0])
        # print('obj'+obj[1])
        if len(obj[1]) > 4:
            a = obj[1][:3] + '···'
            b = obj[1]
        else:
            a = obj[1]
            b = a
        # print(obj)
        data_dic = {
            'num': [obj[0], c],
            'title': a,
            'id': obj[2],
            'view': obj[3],
            'content': obj[4],
            'times': obj[5],
            'photo': get_image,
            'realtitle': b
        }
        text_list.append(data_dic)
    # print(text_list)
    cursor.close()
    conn.close()
    return jsonify(text_list)

def deletes(i):
    if request.method == 'DELETE':
        data = i
        print(data)
        sql = "DELETE FROM photobook WHERE num = %s" %data
        print(sql)
        cursor, conn = db()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return {'':''}
def send_discord_webhook(embed_data):
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'embeds': [embed_data]
    }
    response = requests.post('https://discord.com/api/webhooks/1226373912062066688/v5h7T1IfAF9kg4YpGMH27YPmdiVNndhdhKXeSYl_GGsAlEbj2inwuHxcb5LrniN1iFav', data=json.dumps(payload))
    if response.status_code == 200:
        print('Webhook sent successfully')
    else:
        print(f'Failed to send webhook. Status code: {response.status_code}, Response: {response.text}')


def psmentscollecs(i):
    data = request.get_json()
    data = data['coments']
    sql = "INSERT INTO comentsb (coment, num, id, tim, timekey) VALUES ('%s', '%s', '%s', '%s', '%s')" %(data['ment'], data['num'][0], data['id'], time.strftime('%Y-%m-%d/%I:%M', time.localtime(time.time())), time.time())
    cursor, conn = db()
    cursor.execute(sql)
    conn.commit()
    sql = "SELECT timekey, tim, coment, id, num FROM comentsb WHERE num = %s ORDER BY timekey DESC"%data['num'][0]
    cursor.execute(sql)
    c=dict()
    s=[]
    d=cursor.fetchall()
    for a in d:
        x = c[a[0]] = [a[1],a[2],a[3]]
        s.append(x)
    cursor.close()
    conn.close()
    return {'num':data['num'], 'ment':s}
def gmentscollecs(i):
    data = i
    sql = "SELECT timekey, tim, coment, id, num FROM comentsb WHERE num = %s ORDER BY timekey DESC"%data
    cursor, conn = db()
    cursor.execute(sql)
    c=dict()
    s=[]
    d=cursor.fetchall()
    sql = "SELECT view FROM photobook WHERE num = %s"%data
    cursor.execute(sql)
    view = cursor.fetchall()
    view= int(view[0][0]) + 1
    sql = "UPDATE photobook SET view = '%s' WHERE num = '%s';" %(view, data)
    cursor.execute(sql)
    conn.commit()
    for a in d:
        x=c[a[0]]=[a[1],a[2], a[3]]
        s.append(x)
        print(s)
    cursor.close()
    conn.close()
    return {'num':data, 'ment':s, 'view' : view}

def photodelement(i):
    data = i
    print(data)
    sql = "DELETE from comentsb WHERE coment = \"%s\" ;" % data
    cursor, conn = db()
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return 'a'

def update():
    now = time.localtime()
    times = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    if request.method == 'POST':
        cursor, conn = db()
        binary_image = request.files['image'].read()
        # with open(request.files, "rb") as image_file:
        #     binary_image = image_file.read()
        binary_image = base64.b64encode(binary_image)
        binary_image = binary_image.decode('utf-8')
        # print(request.files)
        # print(times)
        # image_file.save('./savefile/' + secure_filename(image_file.filename))
        # blob = insertBLOB("C:\\Users\\ssong\\PycharmProjects\\pythonProject\\universe\\savefile\\"+secure_filename(image_file.filename))
        sql = "INSERT INTO photobook ( title, ID, view, content, tiem, photo) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_blob = (request.form['title'], request.form['id'], 0, request.form['content'], times, binary_image)
        result = cursor.execute(sql, insert_blob)
        print(result)
        print(cursor.lastrowid)
        if len(request.form['title']) > 8:
            a = request.form['title'][:7] + '···'
            b = request.form['title']
        else:
            a = request.form['title']
            b = a
        print('a :' + a)
        conn.commit()
        cursor.close()
        conn.close()
        print(binary_image)
        # encoded_string = base64.b64encode(image_file.read())
        return {'num': [cursor.lastrowid, 0], 'title': a, 'views': '0', 'times': times, 'realtitle': b,
                'photo': binary_image}
