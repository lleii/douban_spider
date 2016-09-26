#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN


0.xls模板增加列mi_get
1.函数、变量名整理
2.多余to_xls清理

TODOLIST v2：
1.文件解析：MediaCoder集成
2.xls通过文件名点击播放；
3.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取



BUG:
1.需要登录查询，否则404，如https://movie.douban.com/subject/5912992/


chrome cookie：~/Library/Application Support/Google/Chrome/Default/Cookies 

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

        if f['filename'] in pt:
            f['dirpath'] = '/Volumes/data/pt'
            f['filepath'] = os.path.join(f['dirpath'], f['filename'])
            print(f['filepath'])
        if f['filename'] in tv:
            f['dirpath'] = '/Volumes/data/tv'
            f['filepath'] = os.path.join(f['dirpath'], f['filename'])
            print(f['filepath'])
        if f['filename'] in old:
            f['dirpath'] = '/Volumes/data/old'
            f['filepath'] = os.path.join(f['dirpath'], f['filename'])
            print(f['filepath'])
            f['mi_extname']=''
            f['mi_bitrate']=''
            f['mi_container']=''
            f['mi_duration']=''
            f['mi_fileSize']=''
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

def init(cfg) :
    cfg['mode'] = ''
    #cfg['dir'] = ["/Volumes/data/pt","/Volumes/data/old","/Volumes/data/tv"]
    cfg['dir'] = ["/data/src/py/movie-man"]
    cfg['if'] = "o7.xlsx"
    cfg['of'] = "o8.xlsx"

#删除文件，已观看

        

lll=[
  "The Walking Dead S05E03 720p HDTV x264-ASAP[ettv]",
  "Hercules (2014) 1080p BrRip H264 - YIFY",
  "Dawn.of.the.Planet.of.the.Apes.2014.HDRip.XViD-EVO",
  "The Big Bang Theory S08E06 HDTV XviD-LOL [eztv]",
  "22 Jump Street (2014) 720p BrRip x264 - YIFY",
  "Hercules.2014.EXTENDED.1080p.WEB-DL.DD5.1.H264-RARBG",
  "Hercules.2014.Extended.Cut.HDRip.XViD-juggs[ETRG]",
  "Hercules (2014) WEBDL DVDRip XviD-MAX",
  "WWE Hell in a Cell 2014 PPV WEB-DL x264-WD -={SPARROW}=-",
  "UFC.179.PPV.HDTV.x264-Ebi[rartv]",
  "Marvels Agents of S H I E L D S02E05 HDTV x264-KILLERS [eztv]",
  "X-Men.Days.of.Future.Past.2014.1080p.WEB-DL.DD5.1.H264-RARBG",
  "Guardians Of The Galaxy 2014 R6 720p HDCAM x264-JYK",
  "Marvel's.Agents.of.S.H.I.E.L.D.S02E01.Shadows.1080p.WEB-DL.DD5.1",
  "Marvels Agents of S.H.I.E.L.D. S02E06 HDTV x264-KILLERS[ettv]",
  "Guardians of the Galaxy (CamRip / 2014)",
  "The.Walking.Dead.S05E03.1080p.WEB-DL.DD5.1.H.264-Cyphanix[rartv]",
  "Brave.2012.R5.DVDRip.XViD.LiNE-UNiQUE",
  "Lets.Be.Cops.2014.BRRip.XViD-juggs[ETRG]",
  "These.Final.Hours.2013.WBBRip XViD",
  "Downton Abbey 5x06 HDTV x264-FoV [eztv]",
  "Annabelle.2014.HC.HDRip.XViD.AC3-juggs[ETRG]",
  "Lucy.2014.HC.HDRip.XViD-juggs[ETRG]",
  "The Flash 2014 S01E04 HDTV x264-FUM[ettv]",
  "South Park S18E05 HDTV x264-KILLERS [eztv]",
  "The Flash 2014 S01E03 HDTV x264-LOL[ettv]",
  "The Flash 2014 S01E01 HDTV x264-LOL[ettv]",
  "Lucy 2014 Dual-Audio WEBRip 1400Mb",
  "Teenage Mutant Ninja Turtles (HdRip / 2014)",
  "Teenage Mutant Ninja Turtles (unknown_release_type / 2014)",
  "The Simpsons S26E05 HDTV x264 PROPER-LOL [eztv]",
  "2047 - Sights of Death (2014) 720p BrRip x264 - YIFY",
  "Two and a Half Men S12E01 HDTV x264 REPACK-LOL [eztv]",
  "Dinosaur 13 2014 WEBrip XviD AC3 MiLLENiUM",
  "Teenage.Mutant.Ninja.Turtles.2014.HDRip.XviD.MP3-RARBG",
  "Dawn.Of.The.Planet.of.The.Apes.2014.1080p.WEB-DL.DD51.H264-RARBG",
  "Teenage.Mutant.Ninja.Turtles.2014.720p.HDRip.x264.AC3.5.1-RARBG",
  "Gotham.S01E05.Viper.WEB-DL.x264.AAC",
  "Into.The.Storm.2014.1080p.WEB-DL.AAC2.0.H264-RARBG",
  "Lucy 2014 Dual-Audio 720p WEBRip",
  "Into The Storm 2014 1080p BRRip x264 DTS-JYK",
  "Sin.City.A.Dame.to.Kill.For.2014.1080p.BluRay.x264-SPARKS",
  "WWE Monday Night Raw 3rd Nov 2014 HDTV x264-Sir Paul",
  "Jack.And.The.Cuckoo-Clock.Heart.2013.BRRip XViD",
  "WWE Hell in a Cell 2014 HDTV x264 SNHD",
  "Dracula.Untold.2014.TS.XViD.AC3.MrSeeN-SiMPLE",
  "The Missing 1x01 Pilot HDTV x264-FoV [eztv]",
  "Doctor.Who.2005.8x11.Dark.Water.720p.HDTV.x264-FoV[rartv]",
  "Gotham.S01E07.Penguins.Umbrella.WEB-DL.x264.AAC",
  "One Shot [2014] DVDRip XViD-ViCKY",
  "The Shaukeens 2014 Hindi (1CD) DvDScr x264 AAC...Hon3y",
  "The Shaukeens (2014) 1CD DvDScr Rip x264 [DDR]",
  "Annabelle.2014.1080p.PROPER.HC.WEBRip.x264.AAC.2.0-RARBG",
  "Interstellar (2014) CAM ENG x264 AAC-CPG",
  "Guardians of the Galaxy (2014) Dual Audio DVDRip AVI",
  "Eliza Graves (2014) Dual Audio WEB-DL 720p MKV x264",
  "WWE Monday Night Raw 2014 11 10 WS PDTV x264-RKOFAN1990 -={SPARR",
  "Sons.of.Anarchy.S01E03",
  "doctor_who_2005.8x12.death_in_heaven.720p_hdtv_x264-fov",
  "breaking.bad.s01e01.720p.bluray.x264-reward",
  "Game of Thrones - 4x03 - Breaker of Chains",
  "[720pMkv.Com]_sons.of.anarchy.s05e10.480p.BluRay.x264-GAnGSteR",
  "[ www.Speed.cd ] -Sons.of.Anarchy.S07E07.720p.HDTV.X264-DIMENSION",
  "Community.s02e20.rus.eng.720p.Kybik.v.Kybe",
  "The.Jungle.Book.3D.2016.1080p.BRRip.SBS.x264.AAC-ETRG",
  "Ant-Man.2015.3D.1080p.BRRip.Half-SBS.x264.AAC-m2g",
  "Ice.Age.Collision.Course.2016.READNFO.720p.HDRIP.X264.AC3.TiTAN",
  "Red.Sonja.Queen.Of.Plagues.2016.BDRip.x264-W4F[PRiME]",
  "The Purge: Election Year (2016) HC - 720p HDRiP - 900MB - ShAaNi",
  "War Dogs (2016) HDTS 600MB - NBY",
  "The Hateful Eight (2015) 720p BluRay - x265 HEVC - 999MB - ShAaN"
]


def douban_fetch(o,cfg,aa) :

    for index in o.index:
        #f = o.iloc[index]
        #f = o.ix[index,] 

        if o.ix[index,"filename"] not in aa:
            o.set_value(index, "status", "done")
            print(o.ix[index,"filename"],"is done")


        #if index != 150 :
        #    continue

        #已抓取，跳过
        #

        if cfg['mode'] != 'all' and o.ix[index,"db_fetch"] == 1 :
            continue

        #print("Fetching:",index)#保留
        #print(o.set_value(index, "filename"])#保留

        #手工矫正ID
        #if row["id"] is not None and row['status'] != "new":
        #    f = row.to_dict()
         
        if pd.isnull(o.ix[index, "id"]):
        #else : #搜索获取ID
            o.set_value(index, "search_url", "http://api.douban.com/v2/movie/search?q=" + o.ix[index, "title"].replace(' ','%20'))
            search_rst = requests.get(o.ix[index, "search_url"]).json()
            time.sleep(1)#豆瓣:150次/min

            if 'total' in search_rst and search_rst["total"] > 0 :
                o.set_value(index, "id", search_rst["subjects"][0]["id"])

        #抓取信息
        if not pd.isnull(o.ix[index, "id"]):            
            pprint ("fetch")
            pprint (o.ix[index, "filename"])
            #sid = o.set_value(index, "id"]
            #if o.set_value(index, "id",= o.set_value(index, "id"] :#not NaN)
            #    sid = int(o.set_value(index, "id"])
            o.set_value(index, "url", "http://api.douban.com/v2/movie/subject/" + str(int(o.ix[index, "id"])))
            #print ("url:",o.set_value(index, "url"])
            j = requests.get(o.ix[index, "url"]).json()
            time.sleep(1)#豆瓣:150次/min
            #pprint(j)
            #n=0

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
                #o.set_value(index, "db_directors", "")
                for x in j["directors"] :
                    xx += x["name"] + ";"
                #o.set_value(index, "db_directors"] 
                o.set_value(index, "db_directors", xx)

            #print(type(j["aka"]))
            #print(o.set_value(index, "db_aka"])
            
            if 'aka' in j:  
                #o.set_value(index,        "db_aka"   ,   j["aka"])
                o.set_value(index,         'db_aka'   ,   j["aka"])
                #o.set_value(index, "db_aka", list())
                o.set_value(index, "db_fetch", 1)
            #print(o.set_value(index, "db_aka"])

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

    col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    o[col].sort_values(['db_rating'],ascending=0).to_excel(cfg['of'])  
            #if n>0: #已抓取
            #    o.set_value(index, "db_fetch", 1)

        
        #print (f)
        #pprint (o.iloc[index])

def dir_scan(o,cfg,aa) :
    b = o["filename"].tolist()
    #   pprint (len(o))

    #for src_dir in cfg['dir']:
    if 1:
        #a += os.listdir(src_dir)

        #新增文件，新下载
        #for ai in os.listdir(src_dir):
        src_dir="__src"
        for ai in lll:

            if re.search("^\.", ai) or re.match("inc", ai):
                #pprint(ai)  
                continue

            aa.append(ai)

            if ai not in b:
                #pprint(ai) 

                f['status'] = "new"

                f['filename'] = ai
                f['dirpath'] = src_dir
                f['filepath'] = os.path.join(src_dir, ai)

                f.update(ptn.PTN().parse(ai))

                if os.path.isdir(f['filepath']) or os.path.splitext(ai)[1].lower() in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                    o = o.append(f, ignore_index=True) 
    col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    o[col].sort_values(['db_rating'],ascending=0).to_excel(cfg['of'])  

                #rb.append(g)
                
            
        
#        pprint (o.tail())
#        pprint (len(o))
        #o=o.append(dfb)

#    for index, f in o.iterrows():  
    #print(len(o))
    #print(o.index)

def mediainfo_get(o,cfg) :
    #for index, row in o.iterrows():  
    for index in o.index:

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
                        #if os.path.getsize(filepath) > 1024*1024*100:
                        if 1:
                            #print("file:" + filepath)
                            #a = os.path.splitext(filename)[1].lower()
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
    col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    o[col].sort_values(['db_rating'],ascending=0).to_excel(cfg['of'])  


def main() :

    aa = list()
    cfg = dict() #config
    #global search_rst,j

    init(cfg)

    o = pd.read_excel(cfg['if'])
    
    dir_scan(o,cfg,aa)

    douban_fetch(o,cfg,aa)

    #mediainfo_get(o,cfg)

    #列排序by col；行排序by db_rating
    col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    o[col].sort_values(['db_rating'],ascending=0).to_excel("o8.xlsx")  

    return    
    #cfg['dir'] = ["/Volumes/data/pt","/Volumes/data/old","/Volumes/data/tv"]
    #pt = os.listdir('/Volumes/data/pt')
    #tv = os.listdir('/Volumes/data/tv')
    #old = os.listdir('/Volumes/data/old')
    for index, row in o.iterrows():  
        f = row.to_dict()

        pprint (f['filepath'])
        if f['filepath'] != f['filepath'] or f['filepath'] is None:
            r.append(f)
            continue 
        if 'mi_duration' in f:
            if f['mi_duration'] == f['mi_duration'] and f['mi_duration'] != 0:
                r.append(f)
                continue


        if os.path.isdir(f['filepath']):
            f['mi_duration'] = 0
            f['mi_fileSize'] = 0
            for dirpath, dirnames, filenames in os.walk(f['filepath']):
                for filename in filenames:                    
                    mi_extname = os.path.splitext(filename)[1].lower()
                    if mi_extname in  ['.mkv','.mp4','.avi','.iso','.rmvb'] :
                        f['mi_extname'] = mi_extname
                        filepath = os.path.join(dirpath, filename)
                        #if os.path.getsize(filepath) > 1024*1024*100:
                        if 1:
                            print("file:" + filepath)
                            #a = os.path.splitext(filename)[1].lower()
                            info = MediaInfo (filename = filepath,cmd ='/usr/local/bin/mediainfo')
                            infoData = info.getInfo()

                            if infoData:
                            
                                if 'bitrate' in infoData:  
                                    f['mi_bitrate'] = int(infoData['bitrate'])//1000#Kbps
                                    o.set_value(index, "mi_get", 1)
                                if 'container' in infoData:
                                    f['mi_container'] = infoData['container']
                                    o.set_value(index, "mi_get", 1)
                                if 'duration' in infoData:
                                    f['mi_duration'] += int(infoData['duration'])//1000//60 #min
                                    o.set_value(index, "mi_get", 1)
                                if 'fileSize' in infoData:
                                    f['mi_fileSize'] += int(infoData['fileSize'])//1024//1024 #MB
                                    o.set_value(index, "mi_get", 1)
                #print (b)
        else:
            info = MediaInfo (filename = f['filepath'],cmd ='/usr/local/bin/mediainfo')
            infoData = info.getInfo()
            f['mi_extname'] = os.path.splitext(f['filename'])[1].lower()
            if infoData:
                if 'bitrate' in infoData:  
                    f['mi_bitrate'] = int(infoData['bitrate'])//1000
                    o.set_value(index, "mi_get", 1)
                if 'container' in infoData:
                    f['mi_container'] = infoData['container']
                    o.set_value(index, "mi_get", 1)
                if 'duration' in infoData:
                    f['mi_duration'] = int(infoData['duration'])//1000//60
                    o.set_value(index, "mi_get", 1)
                if 'fileSize' in infoData:
                    f['mi_fileSize'] = int(infoData['fileSize'])//1024//1024
                    o.set_value(index, "mi_get", 1)

        pprint (f['mi_duration'])
        r.append(f)

        df = pd.DataFrame(r) 
        #列排序    
        col=['db_fetch','mi_get','id','status','filename','db_rating','db_ratings_count','mi_bitrate','mi_duration','mi_fileSize','filepath','dirpath','mi_extname','mi_container','title','db_title','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
        df = df[col]
        #行排序，by豆瓣评分
        df = df.sort_values(['db_rating'],ascending=0)
        df.to_excel("o6.xlsx")  



    return

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
        if cfg['mode'] != 'all' and row["db_fetch"] > 0 :
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
                f["db_fetch"] = 1

        is_done(f,aa)#已观看
        r.append(f)
        time.sleep(1)#豆瓣:150次IO/min

    df = pd.DataFrame(r) 
    #列排序    
    col=['db_fetch','id','status','filename','title','db_title','db_rating','db_ratings_count','db_directors','db_casts','db_countries','db_genres', 'db_subtype','db_year',  'db_summary', 'db_aka', 'db_alt', 'db_collect_count', 'db_comments_count', 'db_current_season',  'db_do_count', 'db_douban_site','db_episodes_count', 'db_id', 'db_images', 'db_mobile_url','db_original_title', 'db_reviews_count', 'db_schedule_url', 'db_seasons_count','db_share_url', 'db_stars',  'db_wish_count', 'durations', 'excess',  'group', 'languages', 'mainland_pubdate', 'photos','popular_reviews', 'pubdates', 'quality', 'resolution', 'search_url','season',  'url', 'website', 'writers','audio', 'codec', 'year','container']
    df = df[col]
    #行排序，by豆瓣评分
    df = df.sort_values(['db_rating'],ascending=0)
    df.to_excel("o.xlsx")   

if __name__ == '__main__':
    main()









