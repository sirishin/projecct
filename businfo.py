import requests
from bs4 import BeautifulSoup
def busnoseon(n):
    url="http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId={0}".format(n)
    dd=[]
    req = requests.get(url)
    # print(1)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.select('busArrivalList'):
        c = {}
        num = i.select('routeId')[0].string
        times = i.select('predictTime1')[0].string
        name = busname(num)
        which = i.select('locationNo1')[0].string
        sitt = i.select('remainSeatCnt1')[0].string
        if sitt == '-1':
            sitt = 'none'
        # print(num, times, name, which, sitt)
        if name == None:
            pass
        else:
            c['time'] = '%s분'%times
            c['sit'] = sitt
            c['name'] = '%s번' % name
            c['which'] = '%s정류장 전'%which
        dd.append(c)
    # print(n)
    return dd

def busname(num):
    # print(num)
    link = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=1234567890&routeId={0}".format(num)
    req = requests.get(link)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    if not soup.select('routeName'):
        # print(2)
        pass
    else:
        # print(soup.select('routeName'))
        name = soup.select('routeName')[0].string
        # print(name)
        return name
