import csv

import requests as rq
import dicttoxml
import json
from bs4 import BeautifulSoup as BS
import re
import time


def getHtml(url="https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%A4%E8%A3%85&start=20&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019"):  # 获取网页html       输入目的网址，返回html文件

    headers = {"Accept": "application/json, text/plain, */*",
               "Connection": "keep-alive",
               "Host": "movie.douban.com",
               "Referer": "https: // movie.douban.com / tag /",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
               }
    data = {
        "sort": "U",
        "range": "0, 10",
        "tags": "电视剧, 古装",
        "start": "20",
        "countries": "中国大陆",
        "year_range": "2019, 2019"
    }
    r = rq.get(url,headers=headers,data=data)
    soup = BS(r.text, 'lxml')
    return soup


def process(soup):  # directors
    content = []
    for i in soup.find_all('data'):
        a = i.find_all('directors')
        for j in range(0, len(a)):
            content.append(a[j].text)
        content.insert(0, "directors")
    return content


def process2(soup):  # rate
    content = []
    for i in soup.find_all('data'):
        a = i.find_all('rate')
        for j in range(0, len(a)):
            content.append(a[j].text)
        content.insert(0, "rate")
    return content


def process3(soup):  # rate
    content = []
    for i in soup.find_all('data'):
        a = i.find_all('title')
        for j in range(0, len(a)):
            content.append(a[j].text)
        content.insert(0, "title")
    return content


# https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%8F%A4%E8%A3%85&start=0&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019
# https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=电影,古装&start=0&countries=中国大陆&year_range=2019,2019
# https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1,%E5%8F%A4%E8%A3%85&start=60&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019
data1 = [2019, 2018, 2010, 2000, 1990, 1980, 1970, 1960, 1]
data2 = [2019, 2018, 2019, 2009, 1999, 1989, 1979, 1969, 1959]
for q in range(0, len(data1)):
    for i in range(0, 20, 20):
        urls = ['https://movie.douban.com/tag/#/?sort=U&range=0,10&tags']
        with open("douban.txt", 'a+') as fp:
            for url in urls:
                fp.write(str(process(getHtml(url))))
                a = str(process(getHtml(url)))
                print(getHtml(url))
            fp.close()
        with open("douban.txt", 'a+') as fp:
            for url in urls:
                fp.write(str(process2(getHtml(url))))
                b = str(process2(getHtml(url)))
            fp.close()
        with open("douban.txt", 'a+') as fp:
            for url in urls:
                fp.write(str(process3(getHtml(url))))
                c = str(process3(getHtml(url)))
            fp.close()
        with open('csv1.csv', mode='w+', encoding='ANSI', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            data3=data1*len(a)
            print(data3)
            content = [a, b, c, data3]
            content1 = []
            contents = []
            for o in range(0, len(content[0])):
                content1.append(content[0][o])
                content1.append(content[1][o])
                content1.append(content[2][o])
                content1.append(content[3][o])
                contents.append(content1)
                print(content1)
                writer.writerow(contents[0])
                print("已写入")
                time.sleep(5)
