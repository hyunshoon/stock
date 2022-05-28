from bs4 import BeautifulSoup
import pandas as pd
from konlpy.tag import Okt
import requests
import matplotlib.font_manager as fm


okt = Okt()
path_font = './data/NanumGothic.ttf'#font_path
path = "./data/stock_text"
font_name = fm.FontProperties(fname=path_font, size=10).get_name()

def urlToList_news_dart(url):
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  li = [i.text for i in soup.find_all("a", class_ = 'tit')]
  return li

def urlTOList_influencer(url):
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  text_list = [i.text for i in soup.find_all("a", class_ = 'name_link')]#text 가져오기
  links = soup.find_all("a", class_ = 'name_link')#링크 가져오기
  link_list = []
  for link in links:
    link_list.append(link['href'])
  return text_list, link_list

def urlTOList_view(url):
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  text_list = [i.text for i in soup.find_all("a", class_ = 'api_txt_lines total_tit _cross_trigger')]#text 가져오기
  links = soup.find_all("a", class_ = 'api_txt_lines total_tit _cross_trigger')#링크 가져오기
  link_list = []
  for link in links:
    link_list.append(link['href'])
  return text_list, link_list

def download_txt(name_list, code_list):
  word_list = []
  for i in range(0,len(name_list)):
    #view,influencer, 네이버뉴스, 네이버공시정보
    urls = [(f'https://search.naver.com/search.naver?where=view&sm=tab_jum&query={name_list[i]}','view'),
          (f'https://search.naver.com/search.naver?where=influencer&sm=tab_jum&query={name_list[i]}','influencer'),
          (f'https://finance.naver.com/item/news_news.naver?code={code_list[i]}&page=&sm=title_entity_id.basic&clusterId=','news'),
          ]
    term_list = []
    for url in urls:
      if url[1]=='view':
        lines = urlTOList_view(url[0])
        term_list += lines[0]
      if url[1]=='influencer':
        lines = urlTOList_influencer(url[0])
        term_list += lines[0]
      if url[1]=='news':
        lines = urlToList_news_dart(url[0])
        term_list += lines
    print(f'{name_list[i]}완료')
    word_list.append(term_list)
  return pd.DataFrame([word_list], columns=name_list)
if __name__ == '__main__':
    stock_list = pd.read_csv('./data/stock_list.csv', index_col=0,encoding='utf-8')
    df = download_txt(stock_list.name[:100], stock_list.ticker[:100])
    df.to_csv(f'{path}/stock_texts.csv', encoding='utf-8')

