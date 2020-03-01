import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# Selectタグが扱えるエレメントに変化させる為の関数を呼び出す
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
import csv


def click_page(page):
    # もし、エラーがでたらプログラム続行
    try:
        # pageのjavascriptを取得
        onclick = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[1]/nav/ul/li[13]/a '.format(page)).get_attribute('onclick')
            # onclick = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[1]/nav/ul/li[{}]/a'.format(page)).get_attribute('onclick')
            # /html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[1]/nav/ul/li[13]/a     nextpage
            #PageNav > table > tbody > tr > td:nth-child(1) > nav > ul > li:nth-child(8) > a
            #PageNav > table > tbody > tr > td:nth-child(1) > nav > ul > li:nth-child(8) > a
        # javascriptを実行できる形に整形
        js_onclick = onclick.replace("javascript:","")
        # javascriptを実行
        driver.execute_script(js_onclick)
        time.sleep(2)
    except Exception as e:
        pass

def click_zhuceban(line):
    # もし、エラーがでたらプログラム続行
    try:
        # ポップアップのjavascriptを取得
        href = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[{}]/td[14]/a'.format(line)).get_attribute('href')
        # javascriptを実行できる形に整形
        js_href = href.replace("javascript:","")
        # javascriptを実行
        driver.execute_script(js_href)
    except Exception as e:
        pass

def extract_text_list(page, line):
    text = ""
    # テキスト取得
    # もし、textが取得できなかったら、Errorをprintし、プログラム続行
    try:
        # HTMLを文字コードをUTF-8に変換してから取得
        html = driver.page_source.encode('utf-8')
        # BeautifulSoupで扱えるようにパース
        soup = BeautifulSoup(html, "html.parser")
        # idがtext_bodyの要素を抽出
        text = soup.select_one("#text_body")
        text = text.text #tag削除　<class 'bs4.element.Tag'>
        # text = Alert(driver).text
        print(text)

        # ポップアップ右上の　ｘ　クリック -> ポップアップ消去
        # xpathが2パターンあるため、tryで網羅
        try:
            # ｘ　のjavascriptを取得
            x = driver.find_element_by_xpath('/html/body/div[3]/span[1]/a')
            # ｘ　のjavascriptを実行し、ポップアップを消す
            driver.execute_script("arguments[0].click();", x)
            time.sleep(2)
        except Exception as e:
            # ｘ　のjavascriptを取得
            x = driver.find_element_by_xpath('/html/body/div[4]/span[1]/a')
                        # ｘ　のjavascriptを実行し、ポップアップを消す
            driver.execute_script("arguments[0].click();", x)
            # time.sleep(2)
            pass
    except Exception as e:
        print("ERROR:page{}, line{}".format(page, line))
        pass
    return text



options = Options()
##################### 自分で設定してね！ #####################
# ChromeのWebDriverオブジェクトを作成する。
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',chrome_options=options)
###########################################################

# Login画面を開く。
driver.get('http://hsk.blcu.edu.cn/Login')
##################### 自分で設定してね！ #####################
ID = "natsuki"
PASS ="asdfasdf"
###########################################################
print('input the verification code')
KEY = input('>> ')

# ログイン
driver.find_element_by_id('input_admin_name').send_keys(ID)
driver.find_element_by_id('input_admin_pwd').send_keys(PASS)
driver.find_element_by_id('input_admin_verify').send_keys(KEY)
driver.find_element_by_id('exec_submit').click() #Enter keyを押す
print('ログイン成功')
time.sleep(2)

# 全篇检索画面に移動
element = driver.find_element_by_id('nav_qpjs')             #全篇檢索をelementに格納
driver.execute_script("arguments[0].click();", element)     #elementをクリック（Javascript起動）
# time.sleep(2)

# 検索条件を設定
##################### 自分で設定してね！ #####################
element_id = 'ksgj'     #考生國際
# nationality_id ='523'   #韓國
# nationality_id ='525'   #日本
# nationality_id ='542'   #越南
# nationality_id ='801'   #澳大利亞
# nationality_id ='821'   #新西蘭
# nationality_id ='634'   #英國
# nationality_id ='922'   #美國
nationality_id ='501'   #中國
###########################################################
Select(driver.find_element_by_id(element_id)).select_by_value(nationality_id)
print("nationality_id: " + nationality_id)
# time.sleep(2)

# 検索ボタンクリック
driver.execute_script("init_url('Index/nav_qpjs_data','0')")
print('検索成功')
# time.sleep(2)

# 註冊版 copy and paste
text_list = []
# pageループ
##################### 自分で設定してね！　range(3, ココ) #####################
# for page in range(3,282):  # 適当に繰り返し。エラーがでたらExcdeption #韓國
# for page in range(3,218):  #日本
# for page in range(3,19):  #越南
# for page in range(3,12):  #澳大利亞
# for page in range(3,4):  #新西蘭
# for page in range(3,11):  #英國
# for page in range(3,11):  #美國
for page in range(3,19):  #中國
###########################################################
    if page ==3:    # 1ページ目
        print("\n1ページ目")
    else:           # 2ページ目以降
        click_page(page)
        print('\n{}ページ目'.format(page-2))
    # page内の行ループ
    for line in range(2,17): # 1行目-15行目（column名を除く）
        print('{}行目'.format(line-1))
        click_zhuceban(line)
        text = extract_text_list(page, line)
        text_list.append([page-2,line-1,text])
        # time.sleep(2)

# csv出力
##################### 自分で設定してね！open(ココ, 'w')  #####################
# with open(r'/Users/natsuki/Desktop/korea.csv', 'w', encoding='utf_8_sig') as f: #韓國
# with open(r'/Users/natsuki/Desktop/japan.csv', 'w', encoding='utf_8_sig') as f:  #日本
# with open(r'/Users/natsuki/Desktop/vietnam.csv', 'w', encoding='utf_8_sig') as f: #越南
# with open(r'/Users/natsuki/Desktop/australia.csv', 'w', encoding='utf_8_sig') as f: #澳大利亞
# with open(r'/Users/natsuki/Desktop/newzealand.csv', 'w', encoding='utf_8_sig') as f: #新西蘭
# with open(r'/Users/natsuki/Desktop/britain.csv', 'w', encoding='utf_8_sig') as f: #英國
# with open(r'/Users/natsuki/Desktop/america.csv', 'w', encoding='utf_8_sig') as f: #美國
with open(r'/Users/natsuki/Desktop/china.csv', 'w', encoding='utf_8_sig') as f: #中國
###########################################################
    writer = csv.writer(f)
    writer.writerows(text_list)
print("CSV出力完了")
driver.quit()  # ブラウザーを終了する。
