import json
import requests
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
def get_url(url):
	res=requests.get(url,headers=headers)
	json_data=json.loads(res.text)
	print(res.text)
	films=json_data.get('subjects')
	for film in films:
			try:
				f.write(film['id']+'\t'+film['rate']+'\t'+film['title']+'\n')
			except:
				f.write('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'+'\n')
				print(film['id'])
				pass
#https://movie.douban.com/tag/#/?sort=U&range=0,10&tags=电视剧,古装,中国大陆,2019
#https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%A4%E8%A3%85&start=0&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019
if __name__=='__main__':
	urls=['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E8%A7%86%E5%89%A7,%E5%8F%A4%E8%A3%85&start={}&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2019,2019'.format(str(i)) for i in range(0,220,20)]#在这里我爬取的是日语的电影
	f=open('douban.txt','a+')
	for url in urls:
		get_url(url)
	f.close()
