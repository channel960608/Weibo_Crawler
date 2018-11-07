# -*- coding: utf-8 -*-
import scrapy
import json
import random
import time
import re

from ..items import WeiboContentItem
import requests
import random
import datetime
from datetime import timedelta

import importlib,sys
importlib.reload(sys)
from .WeiboBaseSpider import WeiboBaseSpider
# sys.setdefaultencoding('utf8')

class WeiboContentSpiderSpider(WeiboBaseSpider):
    name = "weibo_content_spider"
    
    start_users =[1669879400]
    crawl_username = "用户6433252057"
    page = 1

    def start_requests(self):
        self.login()
        # for start_user in self.start_users:
        # 	weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%010d&containerid=107603%010d&page=1"%(start_user, start_user)
        # 	yield scrapy.Request(weibo_page,headers = self.basicInfo_headers, callback= self.parse_weibo, meta={"id":start_user})
        
        f = open('crawl_user.txt')
        ids = f.readlines()
        for start_user in ids:
            start_user = re.sub("\\n", "",start_user)
            weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%s&containerid=107603%s&page=1"%(start_user, start_user)
            yield scrapy.Request(weibo_page,headers = self.basicInfo_headers, callback= self.parse_weibo, meta={"id":start_user})
        f.close()

    def time_standarlize(self, timestr):
        # print (timestr)
        #可能存在的时间：xx分钟前，1小时前，昨天xx:xx，12-11， 2015-12-11
        #因为三天前的信息不存精确时间，所以统一存日期
        if '前' in timestr:
            # print (timestr)
            #xx前
            return datetime.datetime.now().strftime("%Y-%m-%d")
        elif '昨天' in timestr:
            return (datetime.datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif timestr.count('-') == 1:
            return datetime.datetime.now().strftime("%Y")+ '-' + timestr
        elif '刚刚' in timestr:
            return datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            return timestr

    #微博解析
    def parse_weibo(self, response):
        userid = response.meta["id"]
        json_object = json.loads(response.body)
        datas = json_object["data"]["cards"]
        if len(datas) > 0:
            #判断用户是否有数据
            for data in datas:
                 if data["card_type"] == 9:
                    blog = data["mblog"]
                    item = WeiboContentItem()
                    item["userid"] = userid
                    # item["id"] = blog["id"].encode('utf-8')
                    item["id"] = blog["id"]
                    # item["pub_date"] = self.time_standarlize(blog["created_at"].encode('utf-8'))
                    item["pub_date"] = self.time_standarlize(blog["created_at"])
                    pattern = re.compile("'")
                    blogstr = pattern.sub('"', blog["text"])
                    # item["text"] = blogstr.encode('utf-8')
                    item["text"] = blogstr
                    picture = []
                    if ("pics" in blog) :
                        pics = blog["pics"]
                        for pic in pics:
                            # picture.append(pic["url"].encode('utf-8'))
                            picture.append(pic["url"])
                            item["pic"] = str(picture)
                    yield item
                 self.page += 1
                 next_url = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%s&containerid=107603%s&page=%s"%(userid,userid, self.page)
                 time.sleep(1)
                 yield scrapy.Request(next_url, callback= self.parse_weibo, headers = self.basicInfo_headers,meta={"id":userid})
        else:
             self.page = 1