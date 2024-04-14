import threading
import schedule
import time
from flask import Flask
import asyncio              # 웹 소켓 모듈을 선언한다.
import websockets


app = Flask(__name__)

class A:
    def __init__(self):
        self.result = ""
        schedule.every(5).seconds.do(self.message)

        th = threading.Thread(target=self.worker)
        th.start()  # 생성한 스레드를 시작한다

        th1 = threading.Thread(target=self.websocket)
        th1.start()  # 생성한 스레드를 시작한다

    def message(self):
        self.result = "sdaf"
        print("스케쥴 실행중...")

    def worker(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def websocket(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(websockets.serve(self.accept, "0.0.0.0", 8800))
        loop.run_forever();


        # "0.0.0.0" => 서버 pc에 ip 주소를 입력해준다.
        # 0000 => 서버 pc에 포트를 입력 해 준다.
        # start_server = websockets.serve(self.accept, "0.0.0.0", 8800);
        # asyncio.run(start_server)
        # 비동기로 서버를 대기한다.
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(start_server);
        # loop.run_forever();
        # asyncio.set_event_loop(loop)
        # asyncio.get_event_loop().run_until_complete(start_server);
        # asyncio.get_event_loop().run_forever();

    async def accept(self, websocket, path):
        while True:
            try:
                data = await websocket.recv();  # 클라이언트로부터 메시지를 대기한다.
                print("receive : " + data);
                await websocket.send("ws_srv send data = " + data);  # 클라인언트로 echo를 붙여서 재 전송한다.
            except:
                pass

a = A()

@app.route("/")
def hello():
    print("==============")
    print(a.result)
    return "안녕하세요" + a.result

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")