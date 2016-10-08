#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN

0.监控文件变化/60s?,资源&性能优化
1.flask模板

1.cfg['if']不存在,doing,done为空
2.分国家，类型，年份等筛选
3.重复id查找

TODOLIST v2：
1.xls通过文件名点击播放；
2.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取



BUG:
1.需要登录查询，否则404，如https://movie.douban.com/subject/5912992/


chrome cookie：~/Library/Application Support/Google/Chrome/Default/Cookies 

import wget
url ='http://img7.doubanio.com//view//movie_poster_cover//lpst//public//p2155172952.jpg'
filename = wget.download(url,out='/data')


<a href="https://movie.douban.com/subject/1871906/"><img src="http://img7.doubanio.com/view/movie_poster_cover/ipst/public/p2155172952.jpg"/></a>

<a href="file:///Volumes/data/tv/BBC.行星地球.11集全.2006.国粤台英四语.中英字幕￡CMCT木子鱼">地球脉动</a>

https://datatables.net/examples/advanced_init/dom_toolbar.html

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.10.12/datatables.min.css"/>
 
<script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.10.12/datatables.min.js"></script>

'''

import string
import re
import requests
import json,time,csv
from pprint import pprint
import ptn
import os, sys
import numpy as np
import pandas as pd
from mi import MediaInfo
import os.path

import logging

def init(cfg) :
    cfg['mode'] = ''
    cfg['dir'] = ["/Volumes/data/pt","/Volumes/data/old","/Volumes/data/tv"]
    cfg['if'] = "/Volumes/data/pt/mm2.xlsx"
    cfg['of'] = "/Volumes/data/pt/mm2.xlsx"


    
def douban_fetch(o,cfg,aa) :

    for index in o.index:
        logging.info("douban_fetch:"+str(index*100//len(o))+"%, file:"+o.ix[index, "filename"])
        #logging.info("douban_fetch:",int(index)*100//len(o),"%, file:",o.ix[index, "filename"])

        if cfg['mode'] != 'all' and o.ix[index,"db_fetch"] == 1 :
            continue
         
        if pd.isnull(o.ix[index, "id"]):
            o.set_value(index, "search_url", "http://api.douban.com/v2/movie/search?q=" + o.ix[index, "title"].replace(' ','%20'))
            search_rst = requests.get(o.ix[index, "search_url"]).json()
            time.sleep(0.1)#豆瓣:150次/h

            if 'total' in search_rst and search_rst["total"] > 0 :
                o.set_value(index, "id", search_rst["subjects"][0]["id"])

        #抓取信息
        if not pd.isnull(o.ix[index, "id"]):            
            o.set_value(index, "url", "http://api.douban.com/v2/movie/subject/" + str(int(o.ix[index, "id"])))
            j = requests.get(o.ix[index, "url"]).json()
            time.sleep(0.1)#豆瓣:150次/h

            if 'rating' in j: 
                o.set_value(index, "db_rating", j["rating"]["average"])
                o.set_value(index, "db_stars", j["rating"]["stars"])
                o.set_value(index, "db_fetch", 1)

            if 'alt' in j: 
                o.set_value(index, "db_alt", j["alt"])
                o.set_value(index, "db_fetch", 1)


            if 'directors' in j: 
                o.set_value(index, "db_fetch", 1)
                xx = ""
                for x in j["directors"] :
                    xx += x["name"] + ";"
                o.set_value(index, "db_directors", xx)

            
            if 'aka' in j:  
                o.set_value(index,         'db_aka'   ,   j["aka"])
                o.set_value(index, "db_fetch", 1)

            if 'casts' in j: 
                o.set_value(index, "db_fetch", 1)
                xx = ""
                for x in j["casts"] :
                    xx += x["name"] + ";"
                o.set_value(index, "db_casts", xx)

            if 'countries' in j: 
                o.set_value(index, "db_countries", j["countries"])
                o.set_value(index, "db_fetch", 1)
            if 'genres' in j: 
                o.set_value(index, "db_genres", j["genres"] )
                o.set_value(index, "db_fetch", 1)
            if 'summary' in j: 
                o.set_value(index, "db_summary", j["summary"])
                o.set_value(index, "db_fetch", 1)
            if 'collect_count' in j: 
                o.set_value(index, "db_collect_count", j["collect_count"])
                o.set_value(index, "db_fetch", 1)

            if 'comments_count' in j: 
                o.set_value(index, "db_comments_count", j["comments_count"])
                o.set_value(index, "db_fetch", 1)

            if 'current_season' in j: 
                o.set_value(index, "db_current_season", j["current_season"])
                o.set_value(index, "db_fetch", 1)

            if 'do_count' in j: 
                o.set_value(index, "db_do_count", j["do_count"])
                o.set_value(index, "db_fetch", 1)

            if 'douban_site' in j: 
                o.set_value(index, "db_douban_site", j["douban_site"])
                o.set_value(index, "db_fetch", 1)
            if 'episodes_count' in j: 
                o.set_value(index, "db_episodes_count", j["episodes_count"])
                o.set_value(index, "db_fetch", 1)
            if 'id' in j: 
                o.set_value(index, "db_id", j["id"])
                o.set_value(index, "db_fetch", 1)
            if 'images' in j: 
                o.set_value(index, "db_images", j["images"]["small"])
                o.set_value(index, "db_fetch", 1)
            if 'mobile_url' in j: 
                o.set_value(index, "db_mobile_url", j["mobile_url"])
                o.set_value(index, "db_fetch", 1)
            if 'original_title' in j: 
                o.set_value(index, "db_original_title", j["original_title"])
                o.set_value(index, "db_fetch", 1)
            if 'ratings_count' in j: 
                o.set_value(index, "db_ratings_count", j["ratings_count"])
                o.set_value(index, "db_fetch", 1)
            if 'reviews_count' in j: 
                o.set_value(index, "db_reviews_count", j["reviews_count"])
                o.set_value(index, "db_fetch", 1)
            if 'schedule_url' in j: 
                o.set_value(index, "db_schedule_url", j["schedule_url"])
                o.set_value(index, "db_fetch", 1)
            if 'seasons_count' in j: 
                o.set_value(index, "db_seasons_count", j["seasons_count"])
                o.set_value(index, "db_fetch", 1)
            if 'share_url' in j: 
                o.set_value(index, "db_share_url", j["share_url"])
                o.set_value(index, "db_fetch", 1)
            if 'subtype' in j: 
                o.set_value(index, "db_subtype", j["subtype"])
                o.set_value(index, "db_fetch", 1)
            if 'title' in j: 
                o.set_value(index, "db_title", j["title"])
                o.set_value(index, "db_fetch", 1)
            if 'wish_count' in j: 
                o.set_value(index, "db_wish_count", j["wish_count"])
                o.set_value(index, "db_fetch", 1)
            if 'year' in j: 
                o.set_value(index, "db_year", j["year"])
                o.set_value(index, "db_fetch", 1)
            if 'writers' in j: 
                o.set_value(index, "db_writers", j["writers"])
                o.set_value(index, "db_fetch", 1)
            if 'website' in j: 
                o.set_value(index, "db_website", j["website"])
                o.set_value(index, "db_fetch", 1)
            if 'pubdates' in j: 
                o.set_value(index, "db_pubdates", j["pubdates"])
                o.set_value(index, "db_fetch", 1)
            if 'mainland_pubdate' in j: 
                o.set_value(index, "db_mainland_pubdate", j["mainland_pubdate"])
                o.set_value(index, "db_fetch", 1)
            if 'languages' in j: 
                o.set_value(index, "db_languages", j["languages"])
                o.set_value(index, "db_fetch", 1)
            if 'durations' in j: 
                o.set_value(index, "db_durations", j["durations"])
                o.set_value(index, "db_fetch", 1)
            if 'photos' in j: 
                o.set_value(index, "db_photos", j["photos"])
                o.set_value(index, "db_fetch", 1)
            if 'popular_reviews' in j: 
                o.set_value(index, "db_popular_reviews", j["popular_reviews"])
                o.set_value(index, "db_fetch", 1)

        #col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
        #with pd.ExcelWriter(cfg['of']) as writer:
        #    o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='doing')
        #    o[o.status == 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='done')

def dir_scan(o,cfg,aa) :
    b = o["filename"].tolist()
    f = dict()

    for src_dir in cfg['dir']:
        for ai in os.listdir(src_dir):
            if re.search("^\.", ai) or re.match("inc", ai):
                continue

            aa.append(ai)

            if ai not in b:
                f['status'] = "new"

                f['filename'] = ai
                f['dirpath'] = src_dir
                f['filepath'] = os.path.join(src_dir, ai)

                f.update(ptn.PTN().parse(ai))

                if os.path.isdir(f['filepath']) or os.path.splitext(ai)[1].lower() in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                    o = o.append(f, ignore_index=True) 
                    logging.info("dir_scan new item:"+f['filepath'])


    #col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    #with pd.ExcelWriter(cfg['of']) as writer:
    #    o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='doing')
    #    o[o.status == 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='done')
    return o

def mediainfo_get(o,cfg,aa) :
    for index in o.index:
        logging.info("mediainfo_get:"+str(index*100//len(o))+"%, file:"+o.ix[index, "filename"])

        if o.ix[index,"filename"] not in aa:
            o.set_value(index, "status", "done")
            continue

        if o.db_id.tolist().count(o.ix[index,"db_id"]) > 1:
            o.set_value(index, "status", "dup")        

        if cfg['mode'] != 'all' and o.ix[index,"mi_get"] == 1:
            continue

        if pd.isnull(o.ix[index,"filepath"]):
            continue 

        if os.path.isdir(o.ix[index,"filepath"]):
            o.set_value(index, "mi_duration", 0)
            o.set_value(index, "mi_fileSize", 0)
            for dirpath, dirnames, filenames in os.walk(o.ix[index,"filepath"]):
                for filename in filenames:                    
                    mi_extname = os.path.splitext(filename)[1].lower()
                    if mi_extname in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                        o.set_value(index, "mi_extname", mi_extname)
                        filepath = os.path.join(dirpath, filename)

                        info = MediaInfo (filename = filepath,cmd ='/usr/local/bin/mediainfo')
                        infoData = info.getInfo()

                        if infoData:                            
                            if 'bitrate' in infoData:  
                                o.set_value(index, "mi_bitrate", int(infoData['bitrate'])//1000)#Kbps
                                o.set_value(index, "mi_get", 1)
                            if 'container' in infoData:
                                o.set_value(index, "mi_container", infoData['container'])
                                o.set_value(index, "mi_get", 1)
                            if 'duration' in infoData:
                                o.set_value(index, "mi_duration", o.ix[index,"mi_duration"] + int(infoData['duration'])//1000//60 )#min
                                o.set_value(index, "mi_get", 1)
                            if 'fileSize' in infoData:
                                o.set_value(index, "mi_fileSize", o.ix[index,"mi_fileSize"] + int(infoData['fileSize'])//1024//1024)#MB
                                o.set_value(index, "mi_get", 1)
        else:
            o.set_value(index, "mi_extname", os.path.splitext(o.ix[index,"filename"])[1].lower())
            info = MediaInfo (filename = o.ix[index,"filepath"], cmd ='/usr/local/bin/mediainfo')
            infoData = info.getInfo()                
            if infoData:
                if 'bitrate' in infoData:  
                    o.set_value(index, "mi_bitrate", int(infoData['bitrate'])//1000)
                    o.set_value(index, "mi_get", 1)
                if 'container' in infoData:
                    o.set_value(index, "mi_container", infoData['container'])
                    o.set_value(index, "mi_get", 1)
                if 'duration' in infoData:
                    o.set_value(index, "mi_duration", int(infoData['duration'])//1000//60)
                    o.set_value(index, "mi_get", 1)
                if 'fileSize' in infoData:
                    o.set_value(index, "mi_fileSize", int(infoData['fileSize'])//1024//1024)
                    o.set_value(index, "mi_get", 1)
        #col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
        #with pd.ExcelWriter(cfg['of']) as writer:
        #    o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='doing')
        #    o[o.status == 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='done')

import threading
import time

def main() :

    aa = list()
    cfg = dict() #config


    init(cfg)

    o = pd.read_excel(cfg['if'],'doing').append(pd.read_excel(cfg['if'],'done'), ignore_index=True)
    
    o = dir_scan(o,cfg,aa)
    
    douban_fetch(o,cfg,aa)

    mediainfo_get(o,cfg,aa)

    #列排序by col；行排序by db_rating
    col=['db_fetch','mi_get','id','status','db_title','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    with pd.ExcelWriter(cfg['of']) as writer:
        o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='doing')
        o[o.status == 'done'][col].sort_values(['db_rating'],ascending=0).to_excel(writer, sheet_name='done')

    #o[o.status != 'done'][col].sort_values(['db_rating'],ascending=0).to_html(open('doing.html', 'w'))


    
    logging.info("Main timer expiring")
    
    #timer = threading.Timer(30.0, main)
    #timer.start()

    return     

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S'
                        )

    #hello("ll")


    main()
