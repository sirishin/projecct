from bs4 import BeautifulSoup
import requests
import datetime
import re
now= datetime.datetime.now()
tomorrow = now + datetime.timedelta(days=1)
url = 'https://hyoyang.goeic.kr/meal/view.do?menuId=9562&year=%s&month=%s&day=%s' %(now.year,now.month,now.day)
tourl = 'https://hyoyang.goeic.kr/meal/view.do?menuId=9562&year=%s&month=%s&day=%s' %(tomorrow.year,tomorrow.month,tomorrow.day)
print(url)
pattern = r'\([^)]*\)'
def lunchs():
    req = requests.get(url, verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.select('td')[0].get_text().strip() == '식단이 없습니다.':
        return '오늘 급식은 없습니다'
    else:
        a = soup.select('td')[2]
        print(a)
        a = a.select('span')[0].get_text().strip()
        print(a)
        a = str.replace("\"", "")
        z = re.sub(pattern=pattern, repl='', string=a)
        oa = z.split('ㆍ')
        print(oa)
        return oa
def tolunchs():
    req = requests.get(tourl, verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.select('td')[0].get_text().strip() == '식단이 없습니다.':
        return '내일 급식은 없습니다'
    else:
        tolu = soup.select('td')[2]
        print(tolu)
        tolu = tolu.select('span')[0].get_text().strip()
        print(tolu)
        tolu = tolu\
            .replace("\"", "")
        z = re.sub(pattern=pattern, repl='', string=tolu)
        tolu = z.split('ㆍ')
        print(tolu)
        return tolu
# def getLunch():
#     lun={'today':oa, 'tomorru':tolu}
#     print(lun)
#     return lun

