import re
import time
import requests
import csv
from bs4 import BeautifulSoup

def get_urls(base_url, max_page, urls_csv_f_name):
    # url_dict = {"https://matome.naver.jp/topic/1LwWc?page=":480,
    #             "https://matome.naver.jp/topic/1M0hB?page=":790}
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
    
    with open(urls_csv_f_name,'w', encoding='utf_8_sig') as f:
        writer = csv.writer(f)
        writer.writerows(links)
    # print("=======")
    # with open('nobu_renai_url.csv', 'r', encoding='utf_8_sig') as f:
    #     # writer = csv.writer(f)
    #     renai_links = f.read()
    #     print(renai_links)

def scrape(urls_csv_f_name, text_f_name):

    max_page = 10
    # GET URLS FROM EACH FILE
    f_name = urls_csv_f_name
    print("START PROCESS {}".format(f_name))
    links = []
    with open(f_name, 'r', encoding='utf_8_sig') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            links.append(l)  
    # GET A URL FROM "links" 
    for i, base_url in enumerate(links):
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
            ##################################################
            ########### ここだけ変更してください。 ##################
            ##################################################
            # 視覚的に＜ｈ2＞のみ
            tags = ['p']
            classes = ['mdMTMWidget01ItemTtl01View']
            # 全文字情報
            # tags = ['p', 'div']
            # classes = ['mdMTMWidget01ItemTtl01View', 'mdMTMWidget01ItemTweet01View',
            #    'mdMTMWidget01ItemTweet01View', 'mdMTMWidget01ItemComment01View', 'mdMTMWidget01ItemQuote01View', 'mdMTMWidget01ItemCite01View']
            ##################################################
            ########### ここだけ変更してください。 ##################
            ##################################################
            for tag in tags:
                for c in classes:
                    for p in soup.body.find_all(tag, class_=c):
                        temp = p.text.rstrip()
                        temp = temp.strip()
                        if (temp != "") and (temp not in already_in_data):
                            already_in_data.append(temp)
                            ###### ADD TEXT TO RESULT
                            data.append(temp)
            time.sleep(1)
        # WRITE RESULT
        with open('nobu_shinli.txt', 'a', encoding='utf_8_sig') as f:
            for d in data:
                f.write(d)
                f.write("\n")
        print(i, base_url)

##################################################
########### ここだけ変更してください。 ##################
##################################################
# 記事一覧がURL
matome_url      = ""
# 記事一覧が最大ページの値
max_page        = 
# 記事一覧から抽出した、記事URL一覧を保存するファイル名（CSV）
urls_csv_f_name = ".csv"
# 全記事の見た目で<h2>に当たる内容を保存するファイル名（TXT）
text_f_name     = ".txt"

# 例：
# matome_url      = "https://matome.naver.jp/topic/1LwWc"
# max_page        = 480
# urls_csv_f_name = "xxx_urls.csv"
# text_f_name     = "xxx_text.txt"
##################################################
########### ここだけ変更してください。 ##################
##################################################


base_url = matome_url + '?page='
get_urls(base_url, max_page, urls_csv_f_name)
scrape(urls_csv_f_name, text_f_name)
print("done!")
