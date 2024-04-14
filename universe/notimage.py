from flask import jsonify, request
import pymysql.cursors
import time
import requests
import json
def db():
    conn = pymysql.connect(host='183.99.87.90',
            user='root',
            password='swhacademy!',
            db='Hee',
            charset='utf8')
    cursor = conn.cursor()
    return (cursor, conn)

def findee(id, num):
    cursor, conn = db()
    sql = "SELECT COUNT(ananius) FROM comentbox WHERE num = %s" % (num[0])
    cursor.execute(sql)
    b = cursor.fetchall()
    if b[0][0] == 0:
        conn.close()
        cursor.close()
        return 1
    sql = "SELECT ananius FROM comentbox WHERE num = %s and id = '%s'"%(num[0], id)
    cursor.execute(sql)
    a = cursor.fetchall()
    if len(a) != 0:
        conn.close()
        cursor.close()
        return a[0][0]
    else:
        sql = "SELECT MAX(ananius) FROM comentbox WHERE num = %s" % (num[0])
        cursor.execute(sql)
        a = cursor.fetchall()
        a= int(a[0][0])+1
        conn.close()
        cursor.close()
        return a

def need():
    sql = "SELECT * from comunity"
    cursor, conn = db()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    # lucn = lunchs()
    # tolucn = tolunchs()
    sql = "SELECT num, title, ID, views, content, times FROM comunity ORDER BY num desc"
    cursor.execute(sql)
    list_data = cursor.fetchall()
    text_list = []
    for obj in list_data:
        sql2 = "SELECT coment, num FROM comentbox WHERE num = %s" % obj[0]
        cursor.execute(sql2)
        coments = cursor.fetchall()
        c = []
        for a in coments:
            c.append(a[0])
        if len(obj[1]) > 4:
            a = obj[1][:3] + '···'
            b = obj[1]
        else:
            a = obj[1]
            b = a
        data_dic = {
            'num': [obj[0], c],
            'title': a,
            'id': obj[2],
            'views': obj[3],
            'content': obj[4],
            'times': obj[5],
            'realtitle': b
        }
        text_list.append(data_dic)
    cursor.close()
    conn.close()
    return jsonify(text_list)

# def delete(i):
#     if request.method == 'DELETE':
#         data = i
#         print(data)
#         sql = "DELETE FROM comunity WHERE num = %s" % data
#         print(sql)
#         cursor, conn = db()
#         cursor.execute(sql)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return {'': ''}
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

def everything(i):
    if request.method == 'POST':
        now = time.localtime()
        times = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
        data = request.get_json()
        print(data)
        data = data['tc']
        sql = "INSERT INTO comunity ( title, ID, views, content, times) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
        data['title'], data['id'], 0, data['content'], times)
        cursor, conn = db()
        cursor.execute(sql)
        print(cursor.lastrowid)
        if len(data['title']) > 8:
            a = data['title'][:7] + '···'
            b = data['title']
        else:
            a = data['title']
            b = a
        print('a :' + a)
        conn.commit()
        cursor.close()
        conn.close()
        embed_data = {
            'title': 'Example Embed',
            'description': 'This is an example embed sent via Discord webhook.',
            'color': 0xFF5733,  # You can use color codes in decimal or hexadecimal format
            'fields': [
                {'name': 'Field 1', 'value': 'Value 1', 'inline': True},
                {'name': 'Field 2', 'value': 'Value 2', 'inline': True}
            ]
        }
        send_discord_webhook(embed_data)
        return {'num': [cursor.lastrowid, 0], 'title': a, 'views': '0', 'times': times, 'realtitle': b}
    elif request.method == 'PUT':
        data = request.get_json()
        print(data)
        data = data['tc']
        print(data)
        sql = "UPDATE comunity SET title = '%s', content = '%s' WHERE num = '%s';"%(data['title'], data['content'], i)
        cursor, conn = db()
        cursor.execute(sql)
        conn.commit()
        return '2'
    elif request.method == 'DELETE':
        data = i
        print(data)
        sql = "DELETE FROM comunity WHERE num = %s" % data
        print(sql)
        cursor, conn = db()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return {'': ''}


def psmentscollec(i):
    data = request.get_json()
    data = data['coments']
    other = findee(data['id'], data['num'])
    sql = "INSERT INTO comentbox (coment, num, ID, ananius, tim, timekey) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
    data['ment'], data['num'][0], data['id'], other, time.strftime('%Y-%m-%d/%I:%M', time.localtime(time.time())),
    time.time())
    cursor, conn = db()
    cursor.execute(sql)
    conn.commit()
    sql = "SELECT timekey, tim, coment, ananius, num, lkey FROM comentbox WHERE num = %s ORDER BY timekey DESC" % data['num'][
        0]
    cursor.execute(sql)
    c = dict()
    s = []
    d = cursor.fetchall()
    for a in d:
        x = c[a[0]] = [a[1], a[2], a[3], a[5]]
        s.append(x)
    cursor.close()
    conn.close()
    print(s)
    return {'num': data['num'], 'ment': s}

def gmentscollec(i):
    data = i
    sql = "SELECT timekey, tim, coment, ananius, num, ID, lkey FROM comentbox WHERE num = %s ORDER BY timekey DESC" % data
    cursor, conn = db()
    cursor.execute(sql)
    c = dict()
    s = []
    d = cursor.fetchall()
    sql = "SELECT views FROM comunity WHERE num = %s" % data
    cursor.execute(sql)
    views = cursor.fetchall()
    views = int(views[0][0]) + 1
    sql = "UPDATE comunity SET views = '%s' WHERE num = '%s';" % (views, data)
    cursor.execute(sql)
    conn.commit()
    for a in d:
        x = c[a[0]] = [a[1], a[2], a[3],a[5], a[6]]
        s.append(x)
    cursor.close()
    conn.close()
    return {'num': data, 'ment': s, 'view': views}

def delement(i):
    data = i
    print(data)
    sql = "DELETE from comentbox WHERE lkey = %s ;" % data
    cursor, conn = db()
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return 'a'

# def upload(i):
#     now = time.localtime()
#     times = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
#     if i == 'post':
#         data = request.get_json()
#         print(data)
#         data = data['tc']
#         sql = "INSERT INTO comunity ( title, ID, views, content, times) VALUES ( '%s', '%s', '%s', '%s', '%s')" % (
#         data['title'], data['id'], 0, data['content'], times)
#         cursor, conn = db()
#         cursor.execute(sql)
#         print(cursor.lastrowid)
#         if len(data['title']) > 8:
#             a = data['title'][:7] + '···'
#             b = data['title']
#         else:
#             a = data['title']
#             b = a
#         print('a :' + a)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return {'num': [cursor.lastrowid, 0], 'title': a, 'views': '0', 'times': times, 'realtitle': b}
