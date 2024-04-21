import pymysql.cursors
import schedule
import threading
import json
import copy
from flask import Flask, jsonify, request, send_file
import os
import time
import asyncio
import websockets
from profile import pro
from image import start,deletes, psmentscollecs, gmentscollecs, update,photodelement
from notimage import need, psmentscollec, gmentscollec, everything, delement
from businfo import busnoseon
from lunch import lunchs, tolunchs
from login import register,log
from flask_cors import CORS
import sys
import openai
from Weatherimformation import getValue, weather
from datetime import datetime
dt = datetime.now()
sys.path.append('.')
stopFlag = False
app = Flask(__name__)
items = []
wlist = []
rlist = []
app.secret_key = os.urandom(24)
a=[]
openai.api_key = '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'
CORS(app)
starts = time.time()
weather()
oa =lunchs()
tolu = tolunchs()
def db():
    conn = pymysql.connect(host='183.99.87.90',
            user='root',
            password='swhacademy!',
            db='Hee',
            charset='utf8')
    cursor = conn.cursor()
    return (cursor, conn)

@app.route('/api/start', methods=['GET'])
def haee():
    text_list = start()
    return text_list
@app.route('/api/need', methods=['GET'])
def hae():
    text_list = need()
    return text_list
#로그인
@app.route('/api/deletes/<i>', methods=['DELETE'])
def delle(i):
    return deletes(i)

@app.route('/api/identity/<i>', methods=['GET','POST'])
def profile(i):
    return pro(i)

# @app.route('/api/delete/<i>', methods=['DELETE'])
# def dele(i):
#     return delete(i)
#
# @app.route('/api/remake/<i>', methods=['PUT','GET'])
# def rema(i):
#     return remake(i)
@app.route('/api/login', methods=['POST', 'GET'])
def loginapi():
    if request.method == 'POST':
        return log()
@app.route('/api/icon',  methods=['POST', 'GET'])
def busi():
    image_path = 'C:\\Users\\ssong\\PycharmProjects\\pythonProject\\universe\\usicon.jpg'
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/api/mentscollecs/<i>', methods=['POST','GET','DELETE'])
def wantme(i):
    if request.method == 'POST':
        return psmentscollecs(i)
    elif request.method == 'GET':
        return gmentscollecs(i)
    elif request.method == 'DELETE':
        return photodelement(i)
@app.route('/api/mentscollec/<i>', methods=['POST','GET','DELETE'])
def wantmentapi(i):
    if request.method == 'POST':
        return psmentscollec(i)
    elif request.method == 'GET':
        return gmentscollec(i)
    elif request.method == 'DELETE':
        return delement(i)
# @app.route('/api/upload', methods=['POST','GET'])
# def uploadapis():
#     if request.method == 'POST':
#         return upload('post')

@app.route('/api/everything/<i>', methods=['POST','PUT','DELETE'])
def everythin(i):
    everything(i)
    return '132'
@app.route('/api/updata', methods=['POST','GET'])
def uploadapi():
    if request.method == 'POST':
        return update()

@app.route('/api/lunch', methods=['POST', 'GET'])
def lunchapi():
    return {'today':oa, 'tomorru':tolu}

@app.route('/api/register', methods = ['GET','POST'])
def registe():
    if request.method == 'POST':
        return register()
@app.route('/api/weather', methods=['POST','GET'])
def weathersearch():
    di = getValue()
    return di


schedule.every().day.at("17:03:00").do(weather)
def thred():
    while True:
        threading.currentThread().getName()
        schedule.run_pending()
        time.sleep(1)

class WSC:
    result = dict()
    num = 0
    info = dict()
    def __init__(self):
        self.businfos()
        self.websocketss=[]
        th2 = threading.Thread(target=self.websocket)
        th = threading.Thread(target=self.worker)
        th3 = threading.Thread(target=self.resu)
        th.start()
        th2.start()
        th3.start()
        schedule.every(1).minutes.do(self.businfos)
        # print(122)
    # def message(self):
        # self.result = "sdaf"
        # print("schedule running")

    def worker(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def websocket(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(websockets.serve(self.accept, "127.0.0.1", 8800))
        loop.run_forever();
    def businfos(self):
        # print(1232)
        url = "230000041"
        hynics = "230000215"
        icheon = "230001156"
        bubal = "230000865"
        self.cho = busnoseon(url)
        self.apt = busnoseon(hynics)
        self.ic = busnoseon(icheon)
        self.bb = busnoseon(bubal)
        self.result['bb'] = self.bb
        self.result['ic'] = self.ic
        self.result['apt'] = self.apt
        self.result['cho'] = self.cho
        if self.num == 0:
            self.result['type'] = 'businfo'
        else:
            self.result['type'] = 'bus'
        # print(self.result)
            # print(self.resu())
        return 1
    # def help(self):
    def resu(self):
        # print('emfdjdha')
        # loops = asyncio.get_event_loop()
        while True:
            if self.info == self.result:
                # print(id(self.result))
                # print(id(self.info))
                # print('같음')
                pass
            else:
                # print('다름')
                self.info = copy.deepcopy(self.result)
                # self.backdata()
                asyncio.run(self.backdata())
                # loops.run_until_complete(self.backdata())
                # loops.run_forever()
                # print(id(self.info), id(self.result))
                # print('tlfgodehla')
    async def accept(self, websocket, path):
        # while True:
        # print('접속함')
        # self.resu()
        # print(self.info)
        await websocket.send(json.dumps(self.info))
        self.websocketss.append(websocket)
        # print('dnpq')
        # print(self.info)
        # print(self.websocketss)
        # # for b in websocket:
        # print(32)
    async def backdata(self):
        # print(1232131231)
        # print(self.websocketss)
        for b in self.websocketss:
            # print('보내기')
            # print(b)
            # print(self.info)
            try:
                await b.send(json.dumps(self.info))
                # print('보냄')
            except:
                self.websocketss.remove(b)
                # print(self.websocketss)
                # print('error')
                continue
        # try:
        #     # data = await websocket.recv()  # 클라이언트로부터 메시지를 대기한다.
        #     # print("receive : " + data)
        #     a = self.resu()
        #     await websocket.send(json.dumps(a))
        #     print(39)
        # except:
        #     pass

wsc = WSC()

th = threading.Thread(target=thred, name="wea")
th.start()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
