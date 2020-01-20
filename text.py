import requests as rq
from bs4 import BeautifulSoup as BS
import jieba
import time
import sys
import re
import csv
import os


# 2019LPL全明星周末https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=887&meta=all
# 2019 S9全球总决赛https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=870&meta=all
def getHtml(url):  # 获取网页html
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    rs = rq.get(url, headers, timeout=80)
    statusCode = rs.status_code
    if statusCode == 200:
        rs.encoding = 'utf-8'
        return rs.text
    else:
        return "faile to get trl html"


def remove_all(mylist):  # 去除列表中的空字符  返回列表
    mytest = [i for i in mylist if i != '']
    return mytest


def getComments(html):  # 数据处理，将标签除去获取文本内容（最难）
    soup = BS(html, 'html.parser')
    headers = soup.find('thead', class_='').text
    content = [remove_all(headers.split('\n'))]
    for ul in soup.find_all('tr', class_=''):
        a = ul.find_all('a')
        content.append([remove_all(a[0].text.split('\n')), a[1].text.strip(), a[2].text.strip(), a[3].text.strip(),
                        a[4].text.strip()])
    return content


def wTxt2f(txtList, fileName):
    import os
    openWay = 'a' if os.path.exists(fileName) else 'w'
    with open(fileName, openWay, encoding='utf-8') as fp:
        fp.writelines(str(txtList))
    print("write done!!!! %s" % fileName)


def getfilename(html):
    soup = BS(html, 'html.parser')
    headers = soup.find('select', class_='').text
    content = remove_all(headers.split('\n'))
    return content


def gethtml(url):
    if getHtml(url) is not "faile to get trl html":
        html = getHtml(url)
    return html


def Crawler(url):
    html = getHtml(url)
    comment_s = getComments(html)
    txtList = comment_s
    wTxt2f(txtList, 'lol.txt')
    return txtList


def geteid(html):
    soup = BS(html, 'html.parser')
    return soup.find_all('option')


def getlist():
    url = 'https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid='
    html = gethtml(url)
    list = geteid(html)
    list = re.findall('="(.*?)">', str(list))
    for i in range(0, 6):
        list.pop(-1)
    return list


htmls = 'https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=887&meta=all'
filename = getfilename(getHtml(htmls))
j = 0
for i in range(0, len(filename)):  # 建立文件夹
    path = 'C:\\Users\\f3351\\Desktop\\lol\\{}'.format(filename[i])
    if not os.path.exists(path):
        os.makedirs(path)
    ctype_name = filename
    file_name = path + '\\{}.csv'.format(filename[i])
    with open(file_name, mode='w+', encoding='ANSI', newline='') as f:
        print('正在创建文件/ ' + ctype_name[i])
        writer = csv.writer(f, dialect='excel')
        listnum = getlist()
        num = listnum[j]
        url = 'https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=' + str(num) + '&meta=all'
        print("第" + str(num) + "号,开始爬虫并处理")
        content = Crawler(url)
        for i in content:
            writer.writerow(i)
    j += 1
