import pandas as pd
import requests
from bs4 import BeautifulSoup

date = input('날짜를 입력하세요(yyyymmdd)')
url = f'https://news.naver.com/main/list.naver?mode=LS2D&sid2=230&sid1=101&mid=shm&date={date}&page=1'
#20231127 -> 원하는 날짜로 수정

header = {'user-agent': 'Mozilla/5.0'}
html = requests.get(url, headers = header)
soup = BeautifulSoup(html.text, 'html.parser')

link_li = []

for i in range(1,11):
    link_li.append(soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li:nth-of-type(' + str(i) + ') > dl > dt > a')[0].attrs['href'])

for i in range(1, 11):
    link_li.append(soup.select('#main_content > div.list_body.newsflash_body > ul.type06 > li:nth-of-type(' + str(i) + ') > dl > dt > a')[0].attrs['href'])

title_lst = []
description_lst = []
date_lst = []

for link in link_li:
    header = {"user-agent": "Mozilla/5.0"}

    html = requests.get(link, headers=header)
    soup = BeautifulSoup(html.text, 'html.parser')


    title = soup.find('h2', {'id': 'title_area'})
    title_lst.append(title.text)


    description = soup.find('article', {'id': 'dic_area'})
    description = description.text
    description_lst.append(description)

    date = soup.find('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'})
    date = date['data-date-time']
    date_lst.append(date)

df = pd.DataFrame(zip(date_lst, title_lst, description_lst), columns=['date', 'title', 'description'])

