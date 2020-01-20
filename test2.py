import requests as rq
from bs4 import BeautifulSoup as BS
import re
import json
def getHtml(url):  # 获取网页html
    rs = rq.get(url, timeout=80)
    statusCode = rs.status_code
    if statusCode == 200:
        rs.encoding = 'utf-8'
        return rs.text
    else:
        return "faile to get trl html"
def gethtml(url):
    if getHtml(url) is not "faile to get trl html":
        html = getHtml(url)
    return html

def geteid(html):
    soup = BS(html, 'html.parser')
    return soup.find_all('option')

url='https://www.wanplus.com/ajax/statelist/skill?gametype=2&type=hero'
html=gethtml(url)
list = geteid(html)
list=re.findall('="(.*?)">', str(list))
for i in range(0,6):
      list.pop(-1)
print(list)