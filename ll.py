#!/usr/bin/env python2
# -*- coding:utf-8 -*-
'''
功能列表：
1.文件名解析：PTN集成
2.文件解析：MediaCoder集成
3.在线信息抓取：IMDB、DOUBAN

TODOLIST：
1.文件解析：MediaCoder集成
2.在线信息抓取
3.文件列表、导入；增量更新；
4.导出到csv/xls；
5.imdb信息获取，ID来源：1英文名获取；2.豆瓣获取
6.xls中文件名点击播放；

'''


import string
import re
import urllib2
import json,time,csv
from pprint import pprint

def StringRegexReplace(pattern,repl,string):  
    return  re.sub(pattern, repl, string, count=1, flags=re.I)  

def check_contain_chinese(check_str):
     for ch in check_str.decode('utf-8'):
         if u'\u4e00' <= ch <= u'\u9fff':
             return True
     return False

def main() :
    import os, sys

    for file in os.listdir("."):
        print file
    

    #my_spider = DouBanSpider()
    #my_spider.start_spider()
    #for item in my_spider.datas :
    #    print item
    #url2 = "https://movie.douban.com/subject_search?search_text=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C&cat=1002"
    #url2 = "http://api.douban.com/v2/movie/search?q=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C"
    #filenamei = "大话西游I II合集.1994.BluRay.国粤双语.简体中字￡CMCT如烟.mkv"
    #NewString=u'';  
    #RefinedFileName = "大话西游I II合集.1994.BluRay.国粤双语.简体中字￡CMCT如烟.mkv"
    RefinedFileName = "A Chinese Odyssey 1994 1080p Blu-ray x264 DTS-WiKi"
    #RefinedFileName = "2001太空漫游.2001.A.Space.Odyssey.1968.BluRay.1080p.DTS.x264-CHD"
    #RefinedFileName = ""
    #RefinedFileName = ""
    #RefinedFileName = ""
    #RefinedFileName = "dhxyI IIhj.1994.BluRay.gysy.jtzz￡CMCTry.mkv"
    #RefinedFileName=StringRegexReplace(u'(?<=[\.\-_])[^.]*BluRay(?=[\.\-_])','',filenamei)  
    RefinedFileName=StringRegexReplace(u'\d\d\d\d',u'',RefinedFileName)  
    RefinedFileName=StringRegexReplace(u'DTS-WiKi',u'',RefinedFileName)  
    #RefinedFileName=filenamei.replace(u' ',NewString) 
    #name2 = re.findall(r'(.*\.$).*', name)
    #print (RefinedFileName.split(".")[0].split(" ")[0].split("I")[0])
    #print (check_contain_chinese(RefinedFileName))
    print (RefinedFileName)
'''
    url2 = "http://api.douban.com/v2/movie/search?q=A Chinese Odyssey 1994 1080p Blu-ray x264 DTS-WiKi"
    my_page = urllib2.urlopen(url2)#.read().decode("utf-8")
    data = json.load(my_page)
    #print (data)
    #for x in data:
    #    f.writerow([x["count"], 
    #                x["start"]])
    #print data["subjects"][1]["alt"]

    time.sleep(1)
    url3 = "http://api.douban.com/v2/movie/subject/" +data["subjects"][0]["id"]
    my_page3 = urllib2.urlopen(url3)#.read().decode("utf-8")
    data3 = json.load(my_page3)
    for x in data3["casts"] :
        print (x["name"])
#    print (data3["casts"][5]["name"])
    #pprint (data3["casts"])
    #f = csv.writer(open("test.csv", "wb+"))

    #f.writerow(["pk", "model", "codename", "name", "content_type"])
    #f.writerow([data["count"]])
    time.sleep(1)

'''


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









