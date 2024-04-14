import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, date , timedelta
import schedule
import json
import threading
dt = date.today()
yd = timedelta(days=-1)
yd = dt + yd
print(type(yd.strftime("%Y%m%d")))
# y = yd.strftime("%Y%m%d")
c = {}
d = {}
items = []
wlist = []
rlist = []
def weather():
    rlist.clear()
    wlist.clear()
    items.clear()
    rl ='https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey=ZDMu4srGbL6dNMIQjdFq%2FH9rfT3pg0fsyEDjNIhpfNxMLSTnJNMK%2FcCG5CkIuLfp5%2BwAcRdFUpfQaSOhTPBo2g%3D%3D&pageNo=1&numOfRows=1000&dataType=XML&base_date={0}&base_time=0500&nx=69&ny=121'.format(dt.strftime("%Y%m%d"))
    getting = requests.get(rl)
    soups = BeautifulSoup(getting.text, 'html.parser')
    for b in soups.find_all("item"):
        if b.find("category").string == 'TMP':
            day = b.find("fcstdate").string
            if dt.strftime("%Y%m%d") == day:
                Time = b.find("fcsttime").string
                Time = Time[:2]
                Weath = b.find("fcstvalue").string
                wlist.append([Time,Weath])
            if dt.strftime("%Y%m%d") != day:
                continue
            # print(wlist)
        elif b.find("category").string == 'POP':
            day = b.find("fcstdate").string
            if dt.strftime("%Y%m%d") == day:
                Time = b.find("fcsttime").string
                Time= Time[:2]
                rain = b.find("fcstvalue").string
                rlist.append([Time, rain])
            if dt.strftime("%Y%m%d") != day:
                continue
            # print(rlist)

    if  dt.strftime("%H")== "18" :
        url = 'https://apihub.kma.go.kr/api/typ02/openApi/WthrChartInfoService/getSurfaceChart?pageNo=1&numOfRows=10&dataType=XML&code=12&time={0}&authKey=bQ0AqCTxTIqNAKgk8SyK5A'.format(dt.strftime("%Y%m%d"))
    else:
        url = 'https://apihub.kma.go.kr/api/typ02/openApi/WthrChartInfoService/getSurfaceChart?pageNo=1&numOfRows=10&dataType=XML&code=12&time={0}&authKey=bQ0AqCTxTIqNAKgk8SyK5A'.format(yd.strftime("%Y%m%d"))
    resul = requests.get(url)
    soup = BeautifulSoup(resul.text, 'html.parser')
    item = soup.find_all("man-file")

    if item == 'NoneType' or item == []:
        pass
    else:
        print(item)
        if len(item) == 2:
            items.append(item[1].text)
        else:

            items.append(item.text)
        # for a in item:
        #     if a in items:
        #         pass
        #     else:
        #         items.append(a.string)
    # print(items)
    print(type(items),type(wlist), type(rlist))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def getValue():
    di = {'whea': items, 'd': wlist, 'c': rlist}
    # di = json.dumps(di, default=str)
    return di