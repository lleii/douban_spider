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
from bs4 import BeautifulSoup

def StringRegexReplace(pattern,repl,string):  
    return  re.sub(pattern, repl, string, count=1, flags=re.I)  

def check_contain_chinese(check_str):
     for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return True
     return False

def main() :
    

    #for file in os.listdir("."):
     #   print file

    
    #url2 = "https://movie.douban.com/subject_search?search_text=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C&cat=1002"
    #url2 = "http://api.douban.com/v2/movie/search?q=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C"

    #info = ptn.parse('San Andreas 2015 720p WEB-DL x264 AAC-JYK')
    #info = ptn.parse('大话西游I II合集.1994.BluRay.国粤双语.简体中字￡CMCT如烟.mkv')
    #info = ptn.PTN().parse('A Chinese Odyssey 1994 1080p Blu-ray x264 DTS-WiKi')
    info = ptn.PTN().parse('2001太空漫游.2001.A.Space.Odyssey.1968.BluRay.1080p.DTS.x264-CHD')
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
    j["casts"][0] = j["casts"][0]["name"]
    j["casts"][1] = j["casts"][1]["name"]
    j["casts"][2] = j["casts"][2]["name"]
    j["casts"][3] = j["casts"][3]["name"]
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
    pprint (type(j))
    f = pd.DataFrame(r)    

    '''
    j["casts"] = ""
    j["aka"] = ""
    j["countries"] = ""
    j["directors"] = ""
    j["genres"] = ""
    j["rating"] = ""
    j["summary"] = ""
    #j[""] = ""
    '''
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
    f.to_csv("a.csv",encoding="gb18030")
    print (f)
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

if __name__ == '__main__':
    main()









