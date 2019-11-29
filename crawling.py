import requests
from bs4 import BeautifulSoup
kindlist = ['society', 'politics', 'economic', 'foreign', 'culture','entertain','sports','digital' ]

for kind in kindlist:
    print(kind)
    with open(f'{kind}.txt', 'w',  encoding='UTF8') as f:

        for page in range(1,1001):
            print(page)
            res = requests.get(f'https://news.daum.net/breakingnews/{kind}?page={page}')
            if'해당 일자에 데이터가 없습니다.' in res.text:
                print(res.text.find('해당 일자에 데이터가 없습니다.'))
                break
            soup = BeautifulSoup(res.content, 'html.parser')

            #alist = soup.select('#cSub > div > div.section_cate.section_headline > ul.list_mainnews > li>a')
            link = soup.select(' .tit_thumb > a')
            for a in link:
                f.write(f'{a.attrs["href"]}| {a.text}\n' )
