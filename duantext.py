import dicttoxml
import requests as rq
import json
from bs4 import BeautifulSoup as BS
import jieba
import time
import sys
import matplotlib
import matplotlib.pyplot as plt

def getHtml(url):
    headers = {"Accept": "application/json, text/plain, */*",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Host": "movie.douban.com",
               "Referer": "https: // movie.douban.com / tag /",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
               }
    data = {
        "sort": "U",
        "range": "0, 10",
        "tags": "电视剧, 古装",
        "start": "0",
        "countries": "中国大陆",
        "year_range": "2019, 2019"
    }
    rs = rq.get(url,headers=headers,data=data,timeout=80)
    #xml = dicttoxml.dicttoxml(json.loads(rs.text), root=False, attr_type=False, ).decode('utf-8')
    print(rs)
a=getHtml("https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=电视剧,古装&start=0&countries=中国大陆&year_range=2019,2019")
print(a)