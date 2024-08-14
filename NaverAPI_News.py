!pip install beautifulsoup4
import requests
from bs4 import BeautifulSoup
import pandas as pd

import requests
import pandas as pd

def search_news(keyword):
    url = "https://openapi.naver.com/v1/search/news.json"
    header = {
        "X-Naver-Client-Id": "XXXXXX", #발급받은 Client ID와 Secret 사용
        "X-Naver-Client-Secret": "XXXX"
    }
    params = {
        "query": keyword,
        "display": 50
    }

    response = requests.get(url, headers=header, params=params)
    data = response.json()

    news_list = []
    for item in data['items']:
        link = item.get('originallink', '')  # 'originallink'를 사용하여 원본 뉴스 페이지로 이동
        title = item.get('title', '')
        dsc = item.get('description', '')

        # 추가적인 작업: 원본 뉴스 페이지에서 본문을 크롤링하거나 추가적인 요청을 보낼 수 있음

        news = {'Title': title, 'Description': dsc, 'Link': link}
        news_list.append(news)

    df = pd.DataFrame(news_list)
    return df

df = search_news('손흥민')  #예시로 손흥민의 뉴스 내용만 확
