import pandas as pd
import matplotlib.pyplot as plt
from konlpy.tag import Okt
import re
import urllib.request
import zipfile
from lxml import etree
from nltk.tokenize import word_tokenize, sent_tokenize
from wordcloud import WordCloud
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#빈도수 상위 200 단어중에서 선정
stop_words = ['주','관련','주가','주식','전망','분석','종목','투자','및',
             '에스','한국','기업','매매','텍','청약','모주','홀딩스','오늘','아이',
             '제','등','스','에이','티','일지','코','케이','디','사업',
             '특징','정보','이유','황','호','비','관심','일정','일','후기','앤','소식','채용','외','에프','에이치','위','이',
             '엠','피','방법','매수','매도','젠','리','이슈','알','우리','공부','장주','팩',
              '수익','유','메','더','삼','호스','현','신','씨','수','인','역','확인','가격','프로',
              '리포트','곳','그룹','진','용','기','중','주목','트','솔','기대','거래','보고서','세','기준','것','결정',
              '삼성', '현대', '카카오'#그룹 추가
              ]
#전체 종목 corpus 생성
def make_corpus():
  corpus = []
  total_voca = []#단어 빈도 확인용
  for stock in range(len(total_word_df.columns)):
    words = ''
    cleaned = total_word_df.iloc[0,stock].replace("'",'').replace(' ','').replace('[','').replace(']','').split(',')
    cleaned = [okt.nouns(line) for line in cleaned]
    for i in range(len(cleaned)):
        for word in cleaned[i]:
          words = words+' '+word
          total_voca.append(word)
    corpus.append(words)
  return corpus, total_voca

def make_keyword_impact():
    word_matrix_copy = word_matrix
    word_matrix_copy.loc['keyword_impact'] = 0
    for i in range(len(word_matrix.columns)):
        keyword_impact = sum(word_matrix.iloc[:,i])
        word_matrix_copy.iloc[-1, i] = keyword_impact
    keyword_dict = {}
    for i in range(len(word_matrix_copy.columns)):
        keyword_dict[word_matrix_copy.columns[i]] = word_matrix_copy.iloc[-1, i]
    frequent_word = sorted(keyword_dict.items(), key=lambda x: x[1], reverse=True)
    return frequent_word

def make_cosine_matrix(tfidf_matrix):
  cosine_matrix = cosine_similarity(tfidf_matrix , tfidf_matrix)
  cosine_df = pd.DataFrame(cosine_matrix,columns=stock_list.name)
  cosine_df['index'] = stock_list.name
  cosine_df.set_index('index', inplace=True)
  # cosine_df.to_csv(f'{path_oss}/data/cosine_similirity.csv', encoding='utf-8-sig')
  return cosine_df

def show_stocks(keyword, topN):
    print(word_matrix[keyword].sort_values(ascending=False)[:topN])
def show_relation_stocks(keyword, topN):
    print(cosine_df[keyword].sort_values(ascending=False)[:topN])

def make_wordcloud(name, topN):
    try:
        dict_top = dict(word_matrix.loc[name].sort_values(ascending = False)[:topN]*100)
        del dict_top[name]#해당 종목 이름 제거
    except KeyError:pass

    wc = WordCloud(font_path='./data/NanumGothic.ttf', relative_scaling=0.2,background_color='white').generate_from_frequencies(dict_top)
    plt.imshow(wc)
    plt.savefig(f'./png/{name}_wordcloud.png')

if __name__ == '__main__':
    okt = Okt()
    total_word_df = pd.read_csv('./data/stock_text/stock_texts.csv', index_col=0)
    stock_list = pd.read_csv('./data/stock_list.csv', index_col=0)
    corpus, total_voca = make_corpus()

    tfidfv = TfidfVectorizer(stop_words=stop_words).fit(corpus)
    tfidf_matrix = tfidfv.transform(corpus).toarray()

    word_matrix = pd.DataFrame(tfidfv.transform(corpus).toarray(), columns=tfidfv.get_feature_names_out())
    word_matrix['stock_name'] = stock_list['name']
    word_matrix.set_index('stock_name', inplace=True)

    frequent_word = make_keyword_impact()

    cosine_df = make_cosine_matrix(tfidf_matrix)

    ######Execute example########
    #Input: keyword, topN  output: stock_name
    show_stocks('코로나', 15)
    show_stocks('코인', 10)
    show_stocks('게임', 10)
    show_stocks('폭염', 10)
    show_stocks('배당', 10)

    #Input: stock_name, topN output: keyword
    show_relation_stocks('위메이드', 10)
    show_relation_stocks('신일전자', 5)
    show_relation_stocks('데브시스터즈', 5)

    #Input: stock_name,topN output: wordcloud
    make_wordcloud('에쎈테크', 20)
    make_wordcloud('신일전자', 20)
    make_wordcloud('위메이드', 20)
    make_wordcloud('데브시스터즈', 20)
