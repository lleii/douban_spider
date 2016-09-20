#!/usr/bin/env python
# -*- coding:utf-8 -*-
import string
import re
import urllib2
import json,time,csv


def main() :
    
    #my_spider = DouBanSpider()
    #my_spider.start_spider()
    #for item in my_spider.datas :
    #    print item
    #url2 = "https://movie.douban.com/subject_search?search_text=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C&cat=1002"
    url2 = "http://api.douban.com/v2/movie/search?q=%E4%B8%A4%E5%B0%8F%E6%97%A0%E7%8C%9C"
    my_page = urllib2.urlopen(url2)#.read().decode("utf-8")
    data = json.load(my_page)
    print data
    f = csv.writer(open("test.csv", "wb+"))

    f.writerow(["pk", "model", "codename", "name", "content_type"])
    #for x in data:
    #    f.writerow([x["count"], 
    #                x["start"]])
    #print data["subjects"][1]["alt"]
    time.sleep(2)
    #url3 = data["subjects"][1]["alt"]
    #my_page3 = urllib2.urlopen(url3)#.read().decode("utf-8")
    #data3 = json.load(my_page3)
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









