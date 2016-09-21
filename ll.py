#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN

TODOLIST v1：
1.文件列表、导入；增量更新；
2.导出到csv/xls；

TODOLIST v2：
1.文件解析：MediaCoder集成
2.xls中文件名点击播放；
3.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取


'''



import string
import re
import requests
import json,time,csv
from pprint import pprint
import ptn
import os, sys
import pandas as pd
import BeautifulSoup

def StringRegexReplace(pattern,repl,string):  
    return  re.sub(pattern, repl, string, count=1, flags=re.I)  

def check_contain_chinese(check_str):
     for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return True
     return False

def isset(v): 
    try: 
        type (eval(v)) 
    except: 
        return 0 
    else: 
        return 1

def main() :
    

    #for file in os.listdir("."):
     #   print file
    a = os.listdir("/Volumes/data/pt")
    r = []
    for i in a:
        f = ptn.PTN().parse(i)
        #print(i)
        #print(info["title"])
        f["filename"] = i
        #j["filename"] = i
        
        f["search_url"] = "http://api.douban.com/v2/movie/search?q=" + f["title"].replace(' ','%20')
    
        search_rst = requests.get(f["search_url"]).json()
        #pprint (f)
        #pprint (search_rst.json())
        pprint (search_rst)
        #if isset('search_rst["code"]') and search_rst["code"] == "1998" :
         #   return

        if isset('search_rst["total"]') and search_rst["total"] > 0 :
            f["url"] = "http://api.douban.com/v2/movie/subject/" + search_rst["subjects"][0]["id"]
            j = requests.get(f["url"]).json()
            pprint (j)
            

            n=0
            if isset('j["casts"]'): 
                f["db_casts"] = j["casts"]
                n += 1
            if isset('j["aka"]'): 
                f["db_aka"] = j["aka"]
                n += 1
            if isset('j["countries"]'): 
                f["db_countries"] = j["countries"]
                n += 1
            if isset('j["directors"]'):  
                f["db_directors"] = j["directors"] 
                n += 1
            if isset('j["genres"]'): 
                f["db_genres"] = j["genres"] 
                n += 1
            if isset('j["rating"]'): 
                f["db_rating"] = j["rating"] 
                n += 1
            if isset('j["summary"]'): 
                f["db_summary"] = j["summary"]
                n += 1
            if isset('j["rating"]'): 
                f["db_rating"] = j["rating"]["average"]
                n += 1

            if n>0: 
                f["is_fetch"] = true
  

        r.append(f)
        time.sleep(1)
    
    df = pd.DataFrame(r) 
    df.to_excel("out.xlsx")   
    
'''
    info = ptn.PTN().parse('A Chinese Odyssey 1994 1080p Blu-ray x264 DTS-WiKi')
    
    #info = ptn.PTN().parse('2001太空漫游.2001.A.Space.Odyssey.1968.BluRay.1080p.DTS.x264-CHD')
    title= info["title"].replace(' ','%20')
    print (title) # All details that were parsed


    url2 = "http://api.douban.com/v2/movie/search?q=" + title
    print (url2)
    my_page = requests.get(url2)#.read().decode("utf-8")
    #data = json.load(my_page)
    #pprint (my_page.json())
    #for x in data:
    #    f.writerow([x["count"], 
    #                x["start"]])
    #print data["subjects"][1]["alt"]

    time.sleep(1)
    url3 = "http://api.douban.com/v2/movie/subject/" +my_page.json()["subjects"][0]["id"]
    j = requests.get(url3).json()
    k={}
    #j["casts"][0] = j["casts"][0]["name"]
    #j["casts"][1] = j["casts"][1]["name"]
    #j["casts"][2] = j["casts"][2]["name"]
    #j["casts"][3] = j["casts"][3]["name"]
    #k["castsssss"] = j["casts"][3]["name"]

#    j.update({'cast0':j["casts"][0]})
#    j.update({'cast1':j["casts"][1]})
#    j.update({'cast2':j["casts"][2]})
#    j.update({'cast3':j["casts"][3]})

    r = []
    #k["casts"] = j["casts"][0] 

    j["directors"] = j["directors"][0]["name"]
    j["images"] = j["images"]["small"]
    r.append(j)
    #pprint (type(j))
    f = pd.DataFrame(r)    

    
    #j["casts"] = ""
    #j["aka"] = ""
    #j["countries"] = ""
    #j["directors"] = ""
    #j["genres"] = ""
    #j["rating"] = ""
    #j["summary"] = ""
    #j[""] = ""
    
    #data3 = json.load(my_page3)
    
    
    #f = pd.DataFrame({'aka' : j["aka"],
                     #'alt' : j["alt"]}) 
    #f = pd.DataFrame()
    
    #for row in rows:

            #dict1 = {1,2,3}
            ##Blah Blah .... 
            #dict1.update(blah..) 
            #rows_list.append(dict1)
    #print (j["casts"][0])
#    dict1 = {"aka":1,"alt":2,"cast":3}
 #   dict2 = {"a":1,"b":2,"c":5}
  #  r.append(dict1)
   # r.append(dict2)
    #r += j["casts"]
    #f = pd.DataFrame.from_dict(j, orient='index').T.set_index('index')   
    #f = pd.DataFrame(j.items())    
    #f.to_excel("b.xlsx",encoding="gb18030")
    f.to_excel("b.xlsx")
    #print (f)
    #pprint (r)

    #print (type(json.dumps(j)))
    #pd.read_json(json.dumps(j))

    

#    print (data3["casts"][5]["name"])
    #pprint (data3["casts"])
    #f = csv.writer(open("test.csv", "wb+"))

    #f.writerow(["pk", "model", "codename", "name", "content_type"])
    #f.writerow([data["count"]])
    time.sleep(1)




    #print data3
    #time.sleep(1)
    #print data
    #temp_data = []
#    movie_items = re.findall(r'<a href=".*?/subject/(\d*)/"', my_page)
    #for index, item in enumerate(movie_items) :
     #   if item.find("&nbsp") == -1 :
      #      print item
                #temp_data.append("Top" + str(_top_num) + " " + item)
                #_top_num += 1
        #datas.extend(temp_data)

    #print list(enumerate(movie_items))[0]
    #print list(movie_items)[0]
'''
if __name__ == '__main__':
    main()









