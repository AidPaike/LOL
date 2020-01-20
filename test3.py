'''


url = "https://www.wanplus.com/ajax/statelist/skill?gametype=2&type=hero"
data ={
        '_gtk': 474202712,
        'timerange': all,
        'eid': 859,
        'meta': all}
response = rq.post(url,data=data)
'''
import requests
import json
eid = 1
headers = {":authority": "www.wanplus.com",
    ":method": "POST",
    'User-agent':
               r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
               r'AppleWebKit/537.36 (KHTML, like Gecko) '
               r'Chrome/78.0.3904.108 Safari/537.36',
     "origin":"https://www.wanplus.com",
     "x-csrf-token": "474202712",
     "x-requested-with": "XMLHttpRequest",
           }
while True:
    url = 'https://www.wanplus.com/lol/skill/hero?gametype=2&type=hero'
    data = {'_gtk': "474202712",
             'timerange': "all",
            'eid': eid,
            'meta': "all"
            }
    response = requests.post(url, headers=headers,data=data)
    eid +=1
    print(response.text)