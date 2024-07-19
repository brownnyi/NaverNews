import streamlit as st
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
def makePgNum(num):
    if num == 1:
        return num
    elif num == 0:
        return num + 1
    else:
        return num + 9 * (num - 1)

# 크롤링할 url 생성하는 함수 만들기
def makeUrl(search, start_pg, end_pg, sort=1):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search}&start={start_page}&sort={sort}"
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={search}&start={page}&sort={sort}"
            urls.append(url)
        return urls

# html에서 원하는 속성 추출하는 함수 만들기
def news_attrs_crawler(articles, attrs):
    attrs_content = []
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# html생성해서 기사크롤링하는 함수 만들기
def articles_crawler(url):
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    url_naver = html.select(
        "div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver, 'href')
    return url

# 기사 데이터프레임을 반환하는 함수
def get_news_dataframe(search, start_page, end_page, sort=1):
    url = makeUrl(search, start_page, end_page, sort)
    news_url = []
    for i in url:
        urls = articles_crawler(i)
        news_url.extend(urls)

    # NAVER 뉴스만 남기기
    final_urls = []
    for i in tqdm(news_url):
        if "news.naver.com" in i:
           final_urls.append(i)

    news_titles = []
    news_contents = []
    news_dates = []
    for i in tqdm(final_urls):
        news = requests.get(i, headers=headers)
        news_html = BeautifulSoup(news.text, "html.parser")
        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title is None:
            title = news_html.select_one("#content > div.end_ct > div > h2")
        content = news_html.select("article#dic_area")
        if not content:
            content = news_html.select("#articeBody")
        content = ''.join(str(content))
        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')
        news_titles.append(title)
        news_contents.append(content)
        try:
            html_date = news_html.select_one(
                "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
        news_dates.append(news_date)
    news_df = pd.DataFrame({'date': news_dates, 'title': news_titles, 'content': news_contents})
    return news_df

# streamlit 앱
def main():
    st.title("네이버 뉴스 검색 및 요약 앱")

    # 검색어 입력
    search = st.text_input("검색할 키워드를 입력하세요:")

    # 검색 시작할 페이지 입력
    page = st.number_input("크롤링할 시작 페이지를 입력하세요. ex) 1 (숫자만 입력):", 1)

    # 검색 종료할 페이지 입력
    page2 = st.number_input("크롤링할 종료 페이지를 입력하세요. ex) 1 (숫자만 입력):", 1)

    # 시작 버튼 클릭
    go_button = st.button("시작!")

    if go_button:
        if search and page and page2:
            st.info("검색 및 크롤링 중입니다. 잠시 기다려주세요...")
            news_df = get_news_dataframe(search, page, page2)
            st.success("크롤링이 완료되었습니다!")

            # 결과 출력
            st.subheader("크롤링 결과:")
            st.dataframe(news_df, width=1000)

        else:
            st.error("검색어 및 페이지 정보를 모두 입력하세요.")

if __name__ == "__main__":
    main()
