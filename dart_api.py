import OpenDartReader
import pandas as pd
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

stock_list = pd.read_csv('./data/stock_list.csv', encoding='cp1252')
f = open('../dart_API_KEY', 'r')#you should issued a Open Dart API KEY
api_key = f.readline()

dart = OpenDartReader(api_key)

pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
a = dart.list('035420', start = '2021-01-01', end='2022-05-12', kind='A')
a = dart.list('035420', start = '2022-01-01', end='2022-05-12')
txt = dart.document('20220304000687')
print(len(txt))
soup = BeautifulSoup(txt, 'html.parser')
text = soup.text
len(text)
text.replace('\n', '').split(' ')
##문제점. 사업보고서가 감사보고서로 불러와짐
txt = dart.document('20211112001053')
soup = BeautifulSoup(txt, 'html.parser')
text = soup.text
text_list = text.replace('\n', '').split(' ')
len(text_list)

corpus = ''
for txt in text_list:
    corpus = corpus + ' ' + txt
corpus

okt = Okt()
noun_list = okt.nouns(corpus)
noun_list

cnt = Counter(noun_list)
print(cnt)
wc = WordCloud(font_path='./data/NanumGothic.ttf').generate_from_frequencies(cnt)
plt.imshow(wc)