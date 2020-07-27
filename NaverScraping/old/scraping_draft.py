import re
import time
import requests
import csv
from bs4 import BeautifulSoup

# eliminate_text_list = [[\t\n\r\f\v]\n*]]
data = [["BASE_URL","URL","PAGE","TAG","CLASS","TEXT"]]
base_url    = "https://matome.naver.jp/odai/"
article_id  = "2159538700622039301"
max_page    = 5

already_in_data = []
for page in range(1,max_page):
    target_url = "{}{}?page={}".format(base_url, article_id, page)

    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "lxml")

    # TITLE
    if page == 1:
        title = soup.title.text
        data.append([base_url, page, target_url, "title", "", title])
    # BODY
    tags = ['p','div']
    classes = ['mdMTMWidget01ItemTtl01View', 'mdMTMWidget01ItemTweet01View',
            'mdMTMWidget01ItemTweet01View', 'mdMTMWidget01ItemComment01View', 'mdMTMWidget01ItemQuote01View', 'mdMTMWidget01ItemCite01View']
    for tag in tags:
        for c in classes:
            for p in soup.body.find_all(tag, class_=c):
                # print(p.text)
                temp = p.text.rstrip()
                temp = temp.strip()
                # if p.text not in eliminate_text_list:
                if (temp != "") and (temp not in already_in_data):
                    # data.append([target_url, title, page, tag, c ,p.text])
                    already_in_data.append(temp)
                    data.append([base_url, page, target_url, tag, c, temp])
                
    time.sleep(3)
with open('nobu_draft.csv','w', encoding='utf_8_sig') as f:
    writer = csv.writer(f)
    writer.writerows(data)

