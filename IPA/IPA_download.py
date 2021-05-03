## reference #############################################
#  https://qiita.com/denkiuo604/items/f2b6941e1f6a4b108cee
##########################################################

## note ##################################################
# Errorの場合は以下から参照
# https://www.jitec.ipa.go.jp/1_04hanni_sukiru/_index_mondai.html

# "sg":"情報セキュリティマネジメント試験" 2016年より実施開始
# "sc":"情報処理安全確保支援士試験" 2017年より実施開始

# < -2019 >
# 春期のみ実施
# "pm":"プロジェクトマネージャ試験" 
# "db":"データベーススペシャリスト試験" 
# "es":"エンベデッドシステムスペシャリスト試験" 
# "au":"システム監査技術者試験" 
# 秋期のみ実施
# "st":"ITストラテジスト試験" 
# "sa":"システムアーキテクト試験" 
# "nw":"ネットワークスペシャリスト試験" 
# "sm":"ITサービスマネージャ試験" 

# < -2020 >
# 春期のみ実施
# "st":"ITストラテジスト試験" 
# "sa":"システムアーキテクト試験" 
# "nw":"ネットワークスペシャリスト試験" 
# "sm":"ITサービスマネージャ試験" 
# 秋期のみ実施
# "pm":"プロジェクトマネージャ試験" 
# "db":"データベーススペシャリスト試験" 
# "es":"エンベデッドシステムスペシャリスト試験" 
# "au":"システム監査技術者試験" 
###########################################################

import urllib.request
import os

if __name__ == "__main__":
    urlbase = "https://www.jitec.ipa.go.jp/1_04hanni_sukiru/mondai_kaitou_"
    
    exam_type = {   "sg":"情報セキュリティマネジメント試験", 
                    "fe":"基本情報技術者試験", 
                    "ap":"応用情報技術者試験"} 
    for exam, dir_name in exam_type.items():
        print(f"\n[[{dir_name} ({exam})]")
        os.makedirs(dir_name, exist_ok=True)
        season = {1:"h", 2:"a"} # 春期と秋期
        reiwa = False
        for y in range(2009,2022):
            if (exam == "sg") and (y <2016):    # "sg":"情報セキュリティマネジメント試験" 2016年より実施開始
                continue
            for s in range(1,3):
                for t in ["am","pm"]:
                    for qa in ["qs","ans","cmnt"]:
                        
                        if (t == "am") and (qa == "cmnt"): # 講評は午後のみ
                            continue
                        
                        if reiwa == False: 
                            nendo = str(y) + "h" + f'{y-1988:02}' # 例: 2009h21
                        else:
                            nendo = str(y) + "r" + f'{y-2018:02}' # 例: 2020r02
                        page_url = urlbase + nendo + "_" + str(s) + "/"

                        if (y == 2020) and (s == 2):    # 2020年春季 10月試験
                            url     = urlbase + nendo + "_" + "oct" + "/" + nendo + 'o' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        elif (y == 2020) and (s == 1):  # 2020年春季 試験未実施
                            continue
                        elif (y == 2019) and (s == 2):  # 2019年秋季 特別処理 pageurl:h31 url:r01
                            reiwa = True
                            url     = urlbase + str(y) + "h" + f'{y-1988:02}' + "_" + str(s) + "/" + str(y) + "r" + f'{y-2018:02}' + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        elif (y == 2011) and (s == 1):  # 東日本大震災の影響で平成23年度は春期試験が無く，代わりに特別試験が行われた．
                            url     = page_url + nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        else:
                            url     = page_url + nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        
                        try:
                            urllib.request.urlretrieve(url,"{0}/{1}".format(dir_name,filename))
                            print("Success: " + filename)
                        except urllib.error.HTTPError:
                            print("Error: " + url) # ダウンロードできなかったファイル名を表示
    
     
    exam_type = {   "st":"ITストラテジスト試験", 
                    "sa":"システムアーキテクト試験", 
                    "pm":"プロジェクトマネージャ試験", 
                    "nw":"ネットワークスペシャリスト試験", 
                    "db":"データベーススペシャリスト試験", 
                    "es":"エンベデッドシステムスペシャリスト試験", 
                    "sm":"ITサービスマネージャ試験", 
                    "au":"システム監査技術者試験", 
                    "sc":"情報処理安全確保支援士試験"}
    for exam_name, dir_name in exam_type.items():
        print(f"\n[[{dir_name} ({exam_name})]")
        os.makedirs(dir_name, exist_ok=True)
        season = {1:"h", 2:"a"} # 春期と秋期
        reiwa = False
        for y in range(2009,2022):
            if (exam_name == "sc") and (y < 2017): # "sc":"情報処理安全確保支援士試験" 2017年より実施開始
                continue
            if (y >= 2020):
                reiwa = True
            for s in range(1,3):
                if y <= 2019:
                    if ((exam_name == "st")or(exam_name == "sa")or(exam_name == "nw")or(exam_name == "sm")) and (s == 1): # 秋期のみ実施
                        continue
                    if ((exam_name == "pm")or(exam_name == "db")or(exam_name == "es")or(exam_name == "au")) and (s == 2): # 春期のみ実施
                        continue
                else:
                    if ((exam_name == "st")or(exam_name == "sa")or(exam_name == "nw")or(exam_name == "sm")) and (s == 2): # 秋期のみ実施
                        continue
                    if ((exam_name == "pm")or(exam_name == "db")or(exam_name == "es")or(exam_name == "au")) and (s == 1): # 春期のみ実施
                        continue
                for t in ["am1","am2","pm1","pm2"]:
                    for qa in ["qs","ans","cmnt"]:
                        
                        if ("am" in t) and (qa == "cmnt"): # 講評は午後のみ
                            continue
                        
                        if reiwa == False: 
                            nendo = str(y) + "h" + f'{y-1988:02}' # 例: 2009h21
                        else:
                            nendo = str(y) + "r" + f'{y-2018:02}' # 例: 2020r02
                        page_url = urlbase + nendo + "_" + str(s) + "/"
                        
                        if (t == "am1"):
                            exam = "koudo" 
                        else: 
                            exam = exam_name   # am1: 共通試験
                            
                        if (y == 2020) and (s == 2):    # 2020年春季 10月試験
                            url     = urlbase + nendo + "_" + "oct" + "/" + nendo + 'o' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        elif (y == 2020) and (s == 1):  # 2020年春季 試験未実施
                            continue
                        elif (y == 2019) and (s == 2):  # 2019年秋季 特別処理 pageurl:h31 url:r01
                            url     = urlbase + str(y) + "h" + f'{y-1988:02}' + "_" + str(s) + "/" + str(y) + "r" + f'{y-2018:02}' + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        elif (y == 2011) and (s == 1):  # 東日本大震災の影響で平成23年度は春期試験が無く，代わりに特別試験が行われた．
                            url     = page_url + nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + 'tokubetsu' + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        else:
                            url     = page_url + nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                            filename           = nendo + season[s] + "_" + exam + "_" + t + "_" + qa + ".pdf"
                        
                        try:
                            urllib.request.urlretrieve(url,"{0}/{1}".format(dir_name,filename))
                            print("Success: " + filename)
                        except urllib.error.HTTPError:
                            print("Error: " + url) # ダウンロードできなかったファイル名を表示                 