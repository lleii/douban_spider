#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN

TODOLIST v2：
1.文件解析：MediaCoder集成
2.xls通过文件名点击播放；
3.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取

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
        pprint (1)
        return 0 
    else: 
        pprint (2)
        return 1

        
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

def init(cfg) :
    cfg['mode'] = ''
    cfg['dir'] = ["/Volumes/data/pt","/Volumes/data/old","/Volumes/data/tv"]

#删除文件，已观看
def is_done(f,aa) :
    if f["filename"] not in aa:
        f['status'] = "done"
        print(f["filename"])
        return 1        

    return 0
        
from MediaInfo import MediaInfo
import os
import sys
import os.path

'''
    b=set()

    for dirpath, dirnames, filenames in os.walk('/Volumes/data/tv/'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                #if os.path.getsize(filepath) > 1024*1024*100:
                if os.path.splitext(filename)[1] in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                    print("file:" + filepath)
                    print(os.path.getsize(filepath))
                    a = os.path.splitext(filename)[1].lower()
                    b.add(a)

                continue
            print (b)
            
            {'.mp4', '.iso', '.mkv'}
            {'.mkv', '.rmvb', '.mp4'}
            {'.ISO', '.iso', '.mkv', '.mp4'}
            {'.mkv', '.iso', '.mp4'}

                if os.path.splitext(filename)[1] in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                   filepath = os.path.join(dirpath, filename)
                   print("file:" + filepath)
                   print(dirpath)
                   print(dirnames)
                   print(filenames)
                   print(os.path.getsize(filepath))
                   
                   #input_file = open(filepath)
                   #text = input_file.read()
                   #input_file.close()
                   
                   #output_file = open( filepath, 'w')
                   #output_file.write(text)
                   #output_file.close()
'''

def main() :

   
    info     = MediaInfo (filename = '',cmd ='/usr/local/bin/mediainfo')
    infoData = info.getInfo()

    pprint (infoData)

    return
    r = [] #index list
    f = {} #row dict
    g = {}
    a = []
    aa = []
    rb = []
    cfg={} #config
    global search_rst,j

    init(cfg)
    
    o = pd.read_excel("o.xlsx")
    b = o["filename"].tolist()

    for src_dir in cfg['dir']:
        a += os.listdir(src_dir)

    #新增文件，新下载
    for ai in a:
        if re.search("^\.", ai) or re.match("inc", ai):
            #pprint(ai)  
            continue
        if ai not in b:
            pprint(ai) 
            g = {}            
            g['filename'] = ai
            g['status'] = "new"
            rb.append(g)
        aa.append(ai)
    dfb = pd.DataFrame(rb,index= range(len(o),len(o)+len(rb))) 
    o=o.append(dfb)

    for index, row in o.iterrows():  

        #已抓取，跳过
        if cfg['mode'] != 'all' and row["is_fetch"] > 0 :
            f = row.to_dict()
            is_done (f,aa)
            r.append(f)
            continue

        print(index)#保留
        print(row["filename"])#保留

        #手工矫正ID
        if row["id"] is not None and row['status'] != "new":
            f = row.to_dict()
        else : #搜索获取ID
            i=row["filename"]

            f = ptn.PTN().parse(i)
            f["filename"] = i
            if row['status'] == "new":
                f["status"] = "new"

            f["search_url"] = "http://api.douban.com/v2/movie/search?q=" + f["title"].replace(' ','%20')
            search_rst = requests.get(f["search_url"]).json()

            if 'total' in search_rst and search_rst["total"] > 0 :
                f["id"] = search_rst["subjects"][0]["id"]

        #抓取信息
        if 'id' in f and f["id"] is not None:            
            pprint ("fetch")
            pprint (f["filename"])
            sid = f["id"]
            if f["id"] == f["id"] :#not NaN
                sid = int(f["id"])
            f["url"] = "http://api.douban.com/v2/movie/subject/" + str(sid)
            j = requests.get(f["url"]).json()

            n=0

            if 'rating' in j: 
                f["db_rating"] = j["rating"]["average"]
                f["db_stars"] = j["rating"]["stars"]
                n += 1

            if 'alt' in j: 
                f["db_alt"] = j["alt"]
                n += 1

            if 'aka' in j:  
                f["db_aka"] = j["aka"]
                n += 1

            if 'directors' in j: 
                n += 1
                f["db_directors"] = ""
                for x in j["directors"] :
                    f["db_directors"] += x["name"] + ";"

            if 'casts' in j: 
                n += 1
                f["db_casts"] = ""
                for x in j["casts"] :
                    f["db_casts"] += x["name"] + ";"

            if 'countries' in j: 
                f["db_countries"] = j["countries"]
                n += 1
            if 'genres' in j: 
                f["db_genres"] = j["genres"] 
                n += 1
            if 'summary' in j: 
                f["db_summary"] = j["summary"]
                n += 1
            if 'collect_count' in j: 
                f["db_collect_count"] = j["collect_count"]
                n += 1

            if 'comments_count' in j: 
                f["db_comments_count"] = j["comments_count"]
                n += 1

            if 'current_season' in j: 
                f["db_current_season"] = j["current_season"]
                n += 1

            if 'do_count' in j: 
                f["db_do_count"] = j["do_count"]
                n += 1

            if 'douban_site' in j: 
                f["db_douban_site"] = j["douban_site"]
                n += 1
            if 'episodes_count' in j: 
                f["db_episodes_count"] = j["episodes_count"]
                n += 1
            if 'id' in j: 
                f["db_id"] = j["id"]
                n += 1
            if 'images' in j: 
                f["db_images"] = j["images"]["small"]
                n += 1
            if 'mobile_url' in j: 
                f["db_mobile_url"] = j["mobile_url"]
                n += 1
            if 'original_title' in j: 
                f["db_original_title"] = j["original_title"]
                n += 1
            if 'ratings_count' in j: 
                f["db_ratings_count"] = j["ratings_count"]
                n += 1
            if 'reviews_count' in j: 
                f["db_reviews_count"] = j["reviews_count"]
                n += 1
            if 'schedule_url' in j: 
                f["db_schedule_url"] = j["schedule_url"]
                n += 1
            if 'seasons_count' in j: 
                f["db_seasons_count"] = j["seasons_count"]
                n += 1
            if 'share_url' in j: 
                f["db_share_url"] = j["share_url"]
                n += 1
            if 'subtype' in j: 
                f["db_subtype"] = j["subtype"]
                n += 1
            if 'title' in j: 
                f["db_title"] = j["title"]
                n += 1
            if 'wish_count' in j: 
                f["db_wish_count"] = j["wish_count"]
                n += 1
            if 'year' in j: 
                f["db_year"] = j["year"]
                n += 1
            if 'writers' in j: 
                f["db_writers"] = j["writers"]
                n += 1
            if 'website' in j: 
                f["db_website"] = j["website"]
                n += 1
            if 'pubdates' in j: 
                f["db_pubdates"] = j["pubdates"]
                n += 1
            if 'mainland_pubdate' in j: 
                f["db_mainland_pubdate"] = j["mainland_pubdate"]
                n += 1
            if 'languages' in j: 
                f["db_languages"] = j["languages"]
                n += 1
            if 'durations' in j: 
                f["db_durations"] = j["durations"]
                n += 1
            if 'photos' in j: 
                f["db_photos"] = j["photos"]
                n += 1
            if 'popular_reviews' in j: 
                f["db_popular_reviews"] = j["popular_reviews"]
                n += 1
            if n>0: #已抓取
                f["is_fetch"] = 1

        is_done(f,aa)#已观看
        r.append(f)
        time.sleep(1)#豆瓣:150次IO/min

    df = pd.DataFrame(r) 
    #列排序    
    col=['is_fetch','id','status','filename','title','db_title','db_rating','db_ratings_count','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    df = df[col]
    #行排序，by豆瓣评分
    df = df.sort_values(['db_rating'],ascending=0)
    df.to_excel("o.xlsx")   

if __name__ == '__main__':
    main()









