import requests
import re
import json
import csv
import jieba
import wordcloud
import imageio
import matplotlib
import matplotlib.pyplot as plt

#获取网页信息
def getHmtl(url):
    response = requests.get(url,timeout = 10)
    if response.status_code == 200:
        return response.text
    else:
        return None
#对网页进行解析,获得图书的排名、封面、推荐率、书名、作者、卖出次数以及价格。
def parseResult(html):
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)".*?class="name".*?title="(.*?)">.*?class="star">.*?class="tuijian">(.*?)</span>.*?class="publisher_info">.*?target="_blank">(.*?)</a>.*?class="biaosheng">.*?<span>(.*?)</span></div>.*?<p><span\sclass="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'range': item[0],
            'title': item[2],
            'recommend': item[3],
            'author': item[4],
            'times': item[5],
            'price': item[6]
        }#返回item生成器
#将数据写入txt

def write_item_to_file(item):
    with open('./book.txt', 'a', encoding='UTF-8') as f:
        f.write(str(item)+'\n')
        f.close()
    return json.loads(json.dumps(item,ensure_ascii = False))


def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.54.00.00.00.00-month-2019-1-1-' + str(page)
    html = getHmtl(url)
    items = parseResult(html) # 解析过滤我们想要的信息
    csvf = open('book.csv','w',encoding = 'utf-8')
    fileheader = ['range','title','recommend','author','times','price']
    dict_writer = csv.DictWriter(csvf, fileheader)
    dict_writer.writeheader()
    for item in items:
        dict_writer.writerow(write_item_to_file(item))
    csvf.close()

if __name__ == "__main__":
    for i in range(1,6):
        main(i)
