#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN

TODOLIST v1：
1.文件列表、导入；增量更新；
2.导出到csv/xls；
3.status:双向merge：1.增加新项new；2.删除标记为已看done
4.调整列顺序
5.ID手工矫正
6.多目录导入，忽略.~等开头异常文件
7.gitignore xls

TODOLIST v2：
1.文件解析：MediaCoder集成
2.xls中文件名点击播放；
3.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取


b=o["filename"].tolist()

n=0
for i in b :
    if re.search("^\.", i) or re.match("inc", i):
#       continue
        print (i)
        n+=1
        n

'' in b
 p=pd.DataFrame(r,index= numpy.arange(110,112))   

  len(o),len(o)+len(r)

 d = list(set(c) - set(b))

'''



import string
import re
import requests
import json,time,csv
from pprint import pprint
import ptn
import os, sys
import pandas as pd
#import types 
#import BeautifulSoup

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

def init(cfg,r,f) :
    cfg['mode'] = ''

    f["id"] = "原始ID"
    f["audio"] = "音频编码"
    f["codec"] = "视频编码"
    f["container"] = "容器"
    f["excess"] = "其它"
    f["filename"] = "源文件"
    f["group"] = "压制组"
    f["quality"] = "质量分类"
    f["resolution"] = "分辨率"
    f["season"] = "季"
    f["title"] = "标题"
    f["url"] = "API"
    f["year"] = "年份"
    f["search_url"] = "搜索API"

    f["db_rating"] = "豆瓣评分"
    f["db_stars"] = "评星数"
    f["db_alt"] = "条目URL"
    f["db_aka"] = "又名"
    f["db_directors"] = "导演"
    f["db_casts"] = "主演"
    f["db_countries"] = "国家"
    f["db_genres"] = "类型"
    
    
    
    
    
    f["db_douban_site"] = "豆瓣小站"
    
    f["db_id"] = "条目ID"
    f["db_images"] = "海报"
    f["db_mobile_url"] = "移动URL"
    f["db_original_title"] = "原名"

    f["db_ratings_count"] = "评分人数"
    f["db_wish_count"] = "想看人数"
    f["db_do_count"] = "在看人数"
    f["db_collect_count"] = "看过人数"
    f["db_comments_count"] = "短评数"
    f["db_reviews_count"] = "影评数"

    
    f["db_seasons_count"] = "总季数"
    f["db_current_season"] = "当前季数"
    f["db_episodes_count"] = "本季集数"
    f["db_share_url"] = ""
    f["db_schedule_url"] = "影讯URL"
    f["db_subtype"] = "电影电视"
    f["db_title"] = "中文名"
    f["db_summary"] = "简介"
    
    f["db_year"] = "年代"
    f["is_fetch"] = "已抓取"



    f["writers"] = "编剧"
    f["website"] = "官网"
    f["pubdates"] = "上映日期"
    f["mainland_pubdate"] = "大陆上映日期"
    f["languages"] = "语言"
    f["durations"] = "片长"
    f["photos"] = "剧照"
    f["popular_reviews"] = "影评"


    r.append(f)


def main() :
    

    #for file in os.listdir("."):
     #   print file 
     #df = pd.DataFrame() 

    r = [] #index list
    f = {} #row dict
    cfg={} #config
    init(cfg,r,f)
    #pprint (cfg)
    #pprint (r)
    #pprint (f)
    #a = os.listdir("/Volumes/data/pt")
    


    global search_rst,j
    o = pd.read_excel("o4.xlsx")   
#    pprint(o)
    for index, row in o.iterrows():   # 获取每行的index、row
        #for col_name in o.columns:
        if index == 0 :
            continue

        #if index > 1 :
         #   continue  


        if cfg['mode'] != 'all' and row["is_fetch"] > 0 :
            #pprint ("continue")
            r.append(row.to_dict())
            continue

        print(index)#保留
        print(row["filename"])#保留

        #pprint (type(row["id"]))
        #if isinstance(row["id"],str):
        if row["id"] is not None:
            #id = row["id"]
            f = row.to_dict()
            #pprint (f)
            #continue
        else :
            #pprint ("else")
            #pprint (row["id"])
#            pprint (index)
            i=row["filename"]

            f = ptn.PTN().parse(i)
            #print(i)
            #print(info["title"])
            f["filename"] = i
            #j["filename"] = i
            
            f["search_url"] = "http://api.douban.com/v2/movie/search?q=" + f["title"].replace(' ','%20')
            search_rst = requests.get(f["search_url"]).json()

            if 'total' in search_rst and search_rst["total"] > 0 :
                f["id"] = search_rst["subjects"][0]["id"]

            #continue

    
        #return#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


        
        #pprint (f)
        #pprint (search_rst.json())
        #pprint (search_rst)
        #if isset('search_rst["code"]') and search_rst["code"] == "1998" :
         #   return

        #pprint (isset('search_rst["total"]') )
        #pprint (search_rst["total"])

        #if 'total' in search_rst and search_rst["total"] > 0 :
            #f["id"] = search_rst["subjects"][0]["id"]
        #if 'id' in f and isinstance(f["id"],str):
        if 'id' in f and f["id"] is not None:            
#            pprint ("fetch")
            #pprint (f["id"])
            f["url"] = "http://api.douban.com/v2/movie/subject/" + str(f["id"])
            j = requests.get(f["url"]).json()

            #pprint(j)

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
                #f["db_casts"] = j["casts"]
                n += 1
                f["db_directors"] = ""
                for x in j["directors"] :
                    f["db_directors"] += x["name"] + ";"

            if 'casts' in j: 
                #f["db_casts"] = j["casts"]
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


            if n>0: 
                f["is_fetch"] = 1
  

        r.append(f)
        #pprint (f)
        #pprint (r)
        time.sleep(1)

    df = pd.DataFrame(r) 
    col=['is_fetch','id','filename','title','db_title','db_rating','db_ratings_count','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title',  'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    df=df[col]
    df.to_excel("o4.xlsx")   

    #df = pd.DataFrame(r) 
    #df.to_excel("o.xlsx")   


if __name__ == '__main__':
    main()









