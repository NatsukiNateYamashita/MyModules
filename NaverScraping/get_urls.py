import re
import time
import requests
import csv
from bs4 import BeautifulSoup

# url_dict = {"https://matome.naver.jp/topic/1LwWc?page=":480,
#             "https://matome.naver.jp/topic/1M0hB?page=":790}
url_dict = {"https://matome.naver.jp/topic/1M0hB?page=": 790}
for base_url, max_page in url_dict.items():
    # print(base_url, max_page)
    links = []
    for i in range(1,max_page+1):
        target_url = base_url+str(i)
        r = requests.get(target_url)
        soup = BeautifulSoup(r.text, "lxml")
        for aa in soup.select('h3 a'):
            link = aa.get("href")
            print(link)
            links.append([link])
        time.sleep(3)
        
    if base_url == "https://matome.naver.jp/topic/1LwWc?page=":
        with open('nobu_shinli_url.csv','w', encoding='utf_8_sig') as f:
            writer = csv.writer(f)
            writer.writerows(links)
    else:
        with open('nobu_renai_url.csv', 'w', encoding='utf_8_sig') as f:
            writer = csv.writer(f)
            writer.writerows(links)

# print("=======")
# with open('nobu_renai_url.csv', 'r', encoding='utf_8_sig') as f:
#     # writer = csv.writer(f)
#     renai_links = f.read()
#     print(renai_links)


    

