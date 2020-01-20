import csv

import dicttoxml
from bs4 import BeautifulSoup as BS
import requests as rq
import time
import json


def getHtml(url):  # 获取网页html       输入目的网址，返回html文件

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
    r = rq.get(url, headers=headers)
    soup = BS(r.text, 'lxml')
    time.sleep(10)
    return soup


def process(soup):  # directors
    content = []
    for i in soup.find_all('data'):
        a = i.find_all('casts')
        for j in range(0, len(a)):
            content.append(a[j].text)
        content.insert(0, "casts")
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


def main(j, url):
    r = getHtml(url)
    xml = dicttoxml.dicttoxml(json.loads(r.text), root=False, attr_type=False).decode('utf-8')
    soup = BS(xml, 'lxml')
    content = []
    data1 = [2019, 2018, 2010, 2000, 1990, 1980, 1970, 1960, 1]
    for i in range(0, len(process(soup))):
        content.append([process(soup)[i], process2(soup)[i], process3(soup)[i], j])
    print(content)
    with open("最终测试.csv", mode='a', encoding='ANSI', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        for i in content:
            writer.writerow(i)
            f = open('guzhuang.txt', 'a+', encoding='utf-8')
            f.writelines(str(i))
            f.close()


if __name__ == '__main__':
    # https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%A4%E8%A3%85&start=20&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019
    data1 = [2019, 2018, 2010, 2000, 1990, 1980, 1970, 1960, 1]
    data2 = [2019, 2018, 2019, 2009, 1999, 1989, 1979, 1969, 1959]
    for j in range(len(data1)):
        num = [i for i in range(0, 100, 20)]
        urls = []
        for i in num:
            url = "https://movie.douban.com/j/new_search_subjects?" \
                  "sort=U&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%A4%E8%A3%85&start=" + str(i) + "&countries" \
                                                                                                            "=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=" + str(
                data1[j]) + "," + str(data2[j])
            main(data1[j], url)
