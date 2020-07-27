import re
import time
import requests
import csv
from bs4 import BeautifulSoup


max_page = 10
files = ['nobu_shinli_url.csv', 'nobu_renai_url.csv']
# files = ['nobu_shinli_url.csv']
files = ['nobu_renai_url.csv']
# GET URLS FROM EACH FILE
for f_name in files:
    print("START PROCESS {}".format(f_name))
    links = []
    with open(f_name, 'r', encoding='utf_8_sig') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            links.append(l)  
    # GET A URL FROM "links" 
    for i, base_url in enumerate(links[6861:]):
        data = []
        already_in_data = []
        # REQUEST A PAGE AND PARSE  IT
        for page in range(1, max_page):
            target_url = "{}?page={}".format(base_url,page)
            r = requests.get(target_url)
            soup = BeautifulSoup(r.text, "lxml")
            ###### ADD URL AND TITLE TO RESULT
            if page == 1:
                data.append("{}".format(base_url))
                title = soup.title.text
                data.append(title)

            # GET TEXT
            tags = ['p']
            classes = ['mdMTMWidget01ItemTtl01View']
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
                            # data.append([base_url, page, target_url, tag, c, temp])
                            ###### ADD TEXT TO RESULT
                            data.append(temp)

            time.sleep(1)

        # WRITE RESULT
        if f_name == 'nobu_shinli_url.csv':
            with open('nobu_shinli.txt', 'a', encoding='utf_8_sig') as f:
                for d in data:
                    f.write(d)
                    f.write("\n")
        elif f_name == 'nobu_renai_url.csv':
            with open('nobu_renai.txt', 'a', encoding='utf_8_sig') as f:
                for d in data:
                    f.write(d)
                    f.write("\n")
        print(i, base_url)
