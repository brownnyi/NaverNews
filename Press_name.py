#신뢰도 있는 뉴스만 크롤링 하기 위해 언론사 정보를 얻어냄

url = 'https://n.news.naver.com/mnews/article/009/0005224120?sid=106'
res = requests.get(url)

html = res.content
soup = BeautifulSoup(html, 'html.parser')

data = soup.find('img')['alt'] #네이버 뉴스 언론사 정보의 parser들이 제각각이라 언론사 이미지에 있는 언론사 정보를 뽑기 위함


url = makeUrl('제니', 1, 10, 0)
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
presses = []

for i in tqdm(final_urls):
  news = requests.get(i, headers=headers)
  news_html = BeautifulSoup(news.text, "html.parser")
  html = news.content
  soup = BeautifulSoup(html, 'html.parser')
  press = soup.find('img')['alt']
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
  presses.append(press)
  news_titles.append(title)
  news_contents.append(content)
  try:
    html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
    news_date = html_date.attrs['data-date-time']
  except AttributeError:
    news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
    news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
  news_dates.append(news_date)
news_df = pd.DataFrame({'date': news_dates, 'title': news_titles, 'content': news_contents, 'press': presses})
