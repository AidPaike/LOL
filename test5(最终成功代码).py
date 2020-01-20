import requests as rq
import json
import dicttoxml
from bs4 import BeautifulSoup as BS
import re
import os
import csv




"""
author@ 机智如我范
coadjutant @ 王俊琳 杨晨
data@   2019.12.05
site@  中国河北农业大学
etc @ 如有侵权请联系f335125303@163.com

Details : 爬虫：
              本次爬虫网页为：https://www.wanplus.com/lol/skill/hero，目的是获取十年来英雄联盟（LOL）各大赛事，各个英雄出场率等详细信息
              本页面为ajax网页，并且服务器返回json文件，导致无法直接获取页面内容，即便找到变量eid，当换eid访问时，页面直接跳转到初始页面，
              所以决定模拟request header 进行请求并获取json文件，再进行数据处理
          数据处理： 1，文件标题以及csv文件名称都是按照爬取html来获取的，通过简单的处理将文件建立好，同时将eid处理好存入列表，为写入文件时使用
                    2，json文件获取时还需要注意https的SSL 层加密，本次偷懒直接访问了该网页http网页进行请求（后查询只需要把保护的默认值换掉即可），
                        通过简单的正则表达式提取需要内容
                    3，写入CSV文档
运行须知： 只需要将主函数中path写成用户电脑内部路径即可，其他不需要调试（各个库存在情况下）
"""


def getHtml(url):  # 获取网页html       输入目的网址，返回html文件
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    rs = rq.get(url, headers, timeout=80)
    statusCode = rs.status_code
    if statusCode == 200:
        rs.encoding = 'utf-8'
        return rs.text
    else:
        return "faile to get trl html"


def remove_all(mylist):  # 去除列表中的空字符  返回列表    主要用于处理获取的比赛名称时用到
    mytest = [i for i in mylist if i != '']
    return mytest


def getfilename(html):  # 获取文件名称  即比赛名称
    soup = BS(html, 'html.parser')
    headers = soup.find('select', class_='').text
    content = remove_all(headers.split('\n'))
    return content


def clawer(eid):  # 爬取json文件      通过模拟request headers请求获取服务器返回的json文件    并用dicttoxml简单转换格式 并进行Beautifulsoup
    headers = {
        'Host': 'm.wanplus.com',
        'Connection': 'keep-alive',
        'Content-Length': '45',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://m.wanplus.com',
        'X-CSRF-Token': '474202712',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://m.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=7&meta=all',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'wanplus_token=d890ffb57c5ff67ef0cd0c133e47f805; wanplus_storage=lf4m67eka3o; wanplus_sid=97e0bb35d4305d31464d9a3d4709e1d1; UM_distinctid=16eaaf700193a-0726bc486841e5-36664c08-1fa400-16eaaf7001a378; wp_pvid=9088985320; wanplus_csrf=_csrf_tk_407093848; wp_info=ssid=s160029360; Hm_lvt_f69cb5ec253c6012b2aa449fb925c1c2=1575356120,1575359749,1575432863,1575435145; gameType=2; CNZZDATA1275078652=1196580867-1575468752-%7C1575468752; Hm_lpvt_f69cb5ec253c6012b2aa449fb925c1c2=1575473618'
    }
    data = {
        '_gtk': '474202712',
        'timerange': 'all',
        'eid':eid,
        'meta': 'all',
    }
    r = rq.post(
        'http://m.wanplus.com/ajax/statelist/skill?gametype=2&type=hero',
        headers=headers, data=data, timeout=5)
    print(r.text)
    print(type(r.text))
    xml = dicttoxml.dicttoxml(json.loads(r.text), root=False, attr_type=False).decode('utf-8')

    soup = BS(xml, 'lxml')
    return soup


def countherodata(data, soup):  # 英雄名字（中文）heroname                   获取所需要的标签名称  返回标签内容
    soup = clawer(soup)
    a = soup.find_all(data)  # 英雄名字（英文）cpherokey
    countheroname = []  # 英雄出场率 popularity
    for i in range(0, len(a)):  # 英雄被禁率 banrate
        countheroname.append(a[i].text)  # KDA  kda
    return countheroname  # 胜率 winrate


def geteid(html):  # 获取eid 主要为模拟headers时用
    soup = BS(html, 'html.parser')
    return soup.find_all('option')


def gethtml(url):  # 增加复用率
    if getHtml(url) is not "faile to get trl html":
        html = getHtml(url)
    return html


def getlist():  # 获取的eid进行简单处理标签  此处用的简单正则表达式
    url = 'https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid='
    html = gethtml(url)
    list = geteid(html)
    list = re.findall('="(.*?)">', str(list))
    for i in range(0, 6):
        list.pop(-1)
    return list


def processdata(eid):  # 将返回的所有列表组成一个列表便于进行写入文件
    heroname = countherodata('heroname', eid)  # 英雄中文名字
    heroname.insert(0, "heroname")
    cpherokey = countherodata('cpherokey', eid)  # 英雄英文名字
    cpherokey.insert(0, "cpherokey")
    # print(heroname)
    popularity = countherodata('popularity', eid)  # 英雄出场率
    popularity.insert(0, "popularity")
    # print(heroname)
    banrate = countherodata('banrate', eid)  # 被禁率
    banrate.insert(0, "banrate")
    # print(heroname)
    kda = countherodata('kda', eid)  # kda
    kda.insert(0, "kda")
    # print(heroname)
    winrate = countherodata('winrate', eid)  # 胜率
    winrate.insert(0, "winrate")
    # print(heroname)
    content = [heroname, cpherokey, popularity, banrate, kda, winrate]
    contents = []
    for i in range(0, len(heroname)):
        content1 = []
        content1.append(heroname[i])
        content1.append(cpherokey[i])
        content1.append(popularity[i])
        content1.append(banrate[i])
        content1.append(kda[i])
        content1.append(winrate[i])
        contents.append(content1)
    return contents


htmls = 'https://www.wanplus.com/lol/skill/hero?_gtk=474202712&timerange=all&eid=887&meta=all'  # 此处为获取文件名称时爬虫代码（网址）
filename = getfilename(getHtml(htmls))
j = 0
for i in range(0, len(filename)):  # 建立文件夹
    path = 'C:\\Users\\f3351\\Desktop\\lol\\{}'.format(filename[i])
    if not os.path.exists(path):
        os.makedirs(path)
    ctype_name = filename
    file_name = path + '\\{}.csv'.format(filename[i])
    with open(file_name, mode='w+', encoding='ANSI', newline='') as f:  # 开始写入csv文件
        print('正在创建文件/ ' + ctype_name[i])
        writer = csv.writer(f, dialect='excel')
        listnum = getlist()
        num = listnum[j]
        print("第" + str(num) + "号,开始爬虫并处理")
        content = processdata(num)  # 进行模拟 获取服务器json文件并处理
        for i in content:
            writer.writerow(i)
        print("已写入")
    j += 1

# dead code


# for i in range(0,len(a)):  此方法产生数据是str不易分开有效数据
#    print(a[i].text)
# list = list(re.findall('<heroname>(.*?)</heroname>', str( soup.find_all('statelist'))))
# print(list)
# for q in range(0,len(content[0])):
#           for row in range(0,len(content)):
#               writer.write(content[q][row])
#           writer.write("\n")"""
