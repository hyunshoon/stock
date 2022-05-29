import OpenDartReader
import pandas as pd
from bs4 import BeautifulSoup
from konlpy.tag import Okt

def load_dart(code):
    try:
        df = dart.list(code, start='2021-01-01', end='2022-05-12', kind='A')
    except ValueError:
        print('공시 없음')
        return 'no contents'
    txt = dart.document(df.loc[1,'rcept_no'])
    soup = BeautifulSoup(txt, 'html.parser')
    text = soup.text
    text_list = okt.nouns(text.replace('\n', '').split(' '))
    corpus = ''
    for txt in text_list:
        corpus = corpus + ' ' + txt

    print(len(corpus))
    return okt.nouns(corpus)

    # cnt = Counter(noun_list)
    # print(cnt)
    # wc = WordCloud(font_path='./data/NanumGothic.ttf').generate_from_frequencies(cnt)
    # plt.imshow(wc)
if __name__ == '__main__':
    okt = Okt()

    stock_list = pd.read_csv('./data/stock_list.csv', encoding='utf-8', index_col=0)
    f = open('../dart_API_KEY', 'r')  # you should issued a Open Dart API KEY
    api_key = f.readline()
    dart = OpenDartReader(api_key)

    dart_dict = {}
    for i in range(len(stock_list[:50])):
        dart_dict[stock_list.name[i]] = load_dart(stock_list.ticker[i])
        print(i)

    df_dart = pd.DataFrame(dart_dict)