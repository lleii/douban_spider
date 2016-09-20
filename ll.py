#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
һ���򵥵�Python����, ����ץȡ�����ӰTopǰ100�ĵ�Ӱ������

Anthor: Andrew Liu
Version: 0.0.1
Date: 2014-12-04
Language: Python2.7.8
Editor: Sublime Text2
Operate: ��������뿴README.md����
"""
import string
import re
import urllib2
import json,time,csv


class DouBanSpider(object) :
    """��ļ�Ҫ˵��

    ������Ҫ����ץȡ����ǰ100�ĵ�Ӱ����
    
    Attributes:
        page: ���ڱ�ʾ��ǰ������ץȡҳ��
        cur_url: ���ڱ�ʾ��ǰ��ȡץȡҳ���url
        datas: �洢����õ�ץȡ���ĵ�Ӱ����
        _top_num: ���ڼ�¼��ǰ��top����
    """

    def __init__(self) :
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.datas = []
        self._top_num = 1
        print "�����Ӱ����׼������, ׼����ȡ����..."

    def get_page(self, cur_page) :
        """

        ���ݵ�ǰҳ����ȡ��ҳHTML

        Args: 
            cur_page: ��ʾ��ǰ��ץȡ����վҳ��

        Returns:
            ����ץȡ������ҳ���HTML(unicode����)

        Raises:
            URLError:url�������쳣
        """
        url = self.cur_url
        try :
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8")
        except urllib2.URLError, e :
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return my_page

    def find_title(self, my_page) :
        """

        ͨ�����ص�������ҳHTML, ����ƥ��ǰ100�ĵ�Ӱ����

        
        Args:
            my_page: ����ҳ���HTML�ı���������ƥ��
        """
        temp_data = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items) :
            if item.find("&nbsp") == -1 :
                temp_data.append("Top" + str(self._top_num) + " " + item)
                self._top_num += 1
        self.datas.extend(temp_data)
    
    def start_spider(self) :
        """

        �������, ����������ץȡҳ��ķ�Χ
        """
        while self.page <= 4 :
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1

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









