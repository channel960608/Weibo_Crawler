# -*- coding: utf-8 -*-
import scrapy
import json
import random
import time
import re

from ..items import SearchByKeywordItem
import requests
import random
import datetime
from datetime import timedelta

import importlib,sys
importlib.reload(sys)
# sys.setdefaultencoding('utf8')

class SearchByKeywordSpider(scrapy.Spider):
    name = "search_by_keyword"
    start_urls = ['http://m.weibo.cn/api/']

    page = 1
    crawl_username = "用户6433252057"
    current_user = None

    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36']

    login_headers ={
        'User_Agent': random.choice(user_agents),
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Origin': 'https://passport.weibo.cn',
        'Host': 'passport.weibo.cn'
    }

    basicInfo_headers = {
        'User_Agent': random.choice(user_agents),
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Cookie':'',
        'Referer': '',
        'Host': 'm.weibo.cn',
    }

    post_data = {
        'username': '',
        'password': '',
        'savestate': '1',
        'ec': '0',
        'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
        'entry': 'mweibo'
    }
    # 这个入口仍然有效
    login_url = 'https://passport.weibo.cn/sso/login'


    def login(self):
        session = requests.session()
        # username = input(':\n')
        # password = input('请输入密码：\n')
        self.post_data['username'] = "15071300838"
        self.post_data['password'] = "fengqingduo"
        r = session.post(self.login_url, data=self.post_data, headers=self.login_headers)
        if r.status_code != 200:
            raise Exception('模拟登陆失败')
        else:
            print("模拟登陆成功,当前登陆账号为：")
            #模拟登录获得cookie填充到下一步请求的header中
            cookiesDic = requests.utils.dict_from_cookiejar(r.cookies)
            loginCookie = ""
            loginCookie += "SCF" + ':' + cookiesDic['SCF'] + ';'
            loginCookie += "SUB" + ':' + cookiesDic['SUB'] + ';'
            loginCookie += "SUHB" + ':' + cookiesDic['SUHB'] + ';'
            loginCookie += "SSOLoginState" + ':' + cookiesDic['SSOLoginState'] + ';'
            Cookie = "_T_WM=4ce5b7e0381a4c1cda42834cfa39ec95;%sH5_INDEX=3; H5_INDEX_TITLE=%s; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=from=feed&oid=4188537999850167&luicode=20000061&lfid=4188537999850167&fid=1076031976794091&uicode=10000011"%(loginCookie, self.crawl_username)
            self.basicInfo_headers['Cookie'] = Cookie
            self.basicInfo_headers['User_Agent'] = random.choice(self.user_agents),

    def start_requests(self):
        self.login()
        # for start_user in self.start_users:
        #   weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%010d&containerid=107603%010d&page=1"%(start_user, start_user)
        #   yield scrapy.Request(weibo_page,headers = self.basicInfo_headers, callback= self.parse_weibo, meta={"id":start_user})
        #数组存取要爬取的关键词
        key_words =['一带一路']
        for word in key_words:
            word = re.sub("\\n", "",word)
            weibo_page = 'https://m.weibo.cn/api/container/getIndex?type=all&queryVal={}&title={}&containerid=100103type%3D1%26q%3D{}'.format(word,word,word)
            yield scrapy.Request(weibo_page, headers = self.basicInfo_headers, callback= self.parse_weibo, meta={'keyword':word})


    def time_standarlize(self, timestr):
        print (timestr)
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
        keyword = response.meta['keyword']
        json_object = json.loads(response.body)
        datas = json_object["data"]["cards"]
        # print(datas)
        if len(datas) > 0:
            #判断用户是否有数据
            for data in datas:
                 
                 if data["card_type"] == 11:
                    data_in = data["card_group"]
                    for data_in_itr in data_in:
                        print (data_in_itr["card_type"])
                        if data_in_itr["card_type"] == 9:
                            blog = data_in_itr["mblog"]
                            item = SearchByKeywordItem()
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
                 next_url = "https://m.weibo.cn/api/container/getIndex?type=all&queryVal={}&title={}&containerid=100103type%3D1%26q%3D{}&page={}".format(keyword, keyword, keyword, self.page)
                 time.sleep(1)
                 yield scrapy.Request(next_url, callback= self.parse_weibo, headers = self.basicInfo_headers,meta={'keyword':keyword})
        else:
             self.page = 1
