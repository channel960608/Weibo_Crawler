# -*- coding: utf-8 -*-
import scrapy
import json
import random
import time

from ..items import BasicInfoItem
from ..items import WeiboContentItem
import requests
import random
import re

import importlib,sys
importlib.reload(sys)
# sys.setdefaultencoding('utf8')

class WeiboFansSpiderSpider(scrapy.Spider):
    name = "user_info_spider"
    # allowed_domains = ["m.weibo.cn"]
    start_urls = ['http://m.weibo.cn/']

    #基本信息前缀：230283
    #个人主页前缀：100505
    #用户id十位
    start_user = 1000000000
    #用户集合，爬取时得到
    users = set()


    current_user = None

#登录页面https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F

    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36']

    basicInfo_headers = {
        'User_Agent': random.choice(user_agents),
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Cookie':'',
        'Referer': 'https://m.weibo.cn/u/1712539910?uid=1712539910&luicode=20000174',
        'Host': 'm.weibo.cn',
        'X-Requested-With':'XMLHttpRequest'
    }

    login_headers ={
        'User_Agent': random.choice(user_agents),
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
        'Origin': 'https://passport.weibo.cn',
        'Host': 'passport.weibo.cn'
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
        # username = input('请输入用户名:\n')
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
            if 'SCF' not in cookiesDic:
                print("Can not get SCF from cookies")
                raise Exception('Can not get SCF from cookies')
            loginCookie += "SCF" + ':' + cookiesDic['SCF'] + ';'
            loginCookie += "SUB" + ':' + cookiesDic['SUB'] + ';'
            loginCookie += "SUHB" + ':' + cookiesDic['SUHB'] + ';'
            loginCookie += "SSOLoginState" + ':' + cookiesDic['SSOLoginState'] + ';'
            Cookie = "_T_WM=4ce5b7e0381a4c1cda42834cfa39ec95;%s WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode=20000174&lfid=2302831669879400&fid=1005051712539910&uicode=10000011"%(loginCookie)
            self.basicInfo_headers['Cookie'] = Cookie
            self.basicInfo_headers['User_Agent'] = random.choice(self.user_agents),

    def start_requests(self):
        f = open('crawl_user.txt')
        ids = f.readlines()
        self.login()
        #无id，爬取全站
        # while 1:
        #     homepage = "https://m.weibo.cn/u/" + "%010d"%self.start_user
        #     #这里最好用随机数
        #     time.sleep(1)

        #     basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%010d_-_INFO&luicode=10000011&lfid=230283%010d"%(self.start_user, self.start_user)
        #     yield scrapy.Request(basic_info_page, headers = self.basicInfo_headers,callback=self.parse_basicInfo, meta={"id":self.start_user})

        #     #https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=1669879400&containerid=1076031669879400&page=2

        #     #weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%010d&containerid=107603%010d&page=1"%(self.start_user, self.start_user)
        #     # yield scrapy.Request(weibo_page, callback= self.parse_weibo, meta={"id":self.start_user})
        #     self.start_user += 1

        #有id：
        for userid in ids:
            self.current_user = re.sub("\\n", "",userid)

            homepage = "https://m.weibo.cn/u/" + "%s"%self.current_user
            #这里最好用随机数
            time.sleep(1)

            basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s"%(self.current_user, self.current_user)
            yield scrapy.Request(basic_info_page, headers = self.basicInfo_headers,callback=self.parse_basicInfo, meta={"id":self.current_user})

            #https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=1669879400&containerid=1076031669879400&page=2

            #weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%010d&containerid=107603%010d&page=1"%(self.start_user, self.start_user)
            # yield scrapy.Request(weibo_page, callback= self.parse_weibo, meta={"id":self.start_user})
        f.close()

    # def judge_item(self, name, item, item_content):
    #     #传item的引用，直接对item进行修改
    #     if name == "昵称":
    #         item["nickname"] = item_content
    #     elif name == "标签":
    #         item["tags"] = item_content
    #     elif name == "性别":
    #         item["gender"] = item_content
    #     elif name == "所在地":
    #         item["location"] = item_content
    #     elif name == "简介":
    #         item["brief_intro"] = item_content
    #     elif name == "等级":
    #         item["level"] = item_content
    #     elif name == "阳光信用":
    #         item["credit"] = item_content
    #     elif name == "注册时间":
    #         item["signup_date"] = item_content
    #     elif name == "博客":
    #         item["blog"] = item_content
    #     elif name == "公司":
    #         item["company"] = item_content
    #     elif name == "学校":
    #         item["school"] = item_content

    # 重构函数 'judge_item' 避免if语句分支过多的问题
    def judge_item(self, name, item, item_content):
        #传item的引用，直接对item进行修改
        m_dict = {"昵称":"nickname", "标签":"tags","性别":"gender",
            "所在地":"location","简介":"brief_intro", "等级":"level",
             "阳光信用":"credit","博客":"blog",
            "公司":"company","学校":"school"}
        item[m_dict[name]] = item_content


    #个人信息爬取
    def parse_basicInfo(self, response):
        #解析获得个人信息，通过json包获得
        id = response.meta["id"]
        json_object = json.loads(response.body)
        datas = json_object["data"]["cards"]
        print (datas)
        #通过注册日期判断用户是否存在
        #判断获得的数据是否为空
        if datas:
            judge_data = datas[0]["card_group"]

            isUser = True

            #遍历得到注册时间进行判断
            for data in datas:
                basic_data = data["card_group"]
                #通过item_name来判断类型
                for basic_item in basic_data:
                    #签约部分没有item_name
                    if ("item_name" in basic_item) :
                        # item_name = basic_item["item_name"].encode('utf-8')
                        item_name = basic_item["item_name"]
                        # item_content = basic_item["item_content"].encode('utf-8')
                        item_content = basic_item["item_content"]
                        if item_name == "注册时间" and item_content != "1970-01-01":
                            isUser = True
                    else:
                        pass

            if isUser:
                self.users.add(id)
                item = BasicInfoItem()
                item["ID"] = id

                #循环所有的基本信息模块，传参进行判断并赋值
                for data in datas:
                    basic_data = data["card_group"]
                    #通过item_name来判断类型
                    for basic_item in basic_data:
                    #签约部分没有item_name
                        if ("item_name" in basic_item) :
                            # item_name = basic_item["item_name"].encode('utf-8')
                            item_name = basic_item["item_name"]
                            # item_content = basic_item["item_content"].encode('utf-8')
                            item_content = basic_item["item_content"]
                            self.judge_item(item_name, item, item_content)
                        else:
                            pass


                # if 'gender' not in item:
                #     item['gender'] = '无'
                fans_url = "https://m.weibo.cn/api/container/getIndex?uid=%s&luicode=20000174&type=uid&value=%s&containerid=100505%s" % (id, id, id)
                yield scrapy.Request(fans_url, self.parse_fans, meta={"item": item})
            else:
                pass
        else:
            basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s"%(self.current_user, self.current_user)
            yield scrapy.Request(basic_info_page, headers = self.basicInfo_headers,callback=self.parse_basicInfo, meta={"id":self.current_user})

    #微博解析
    '''def parse_weibo(self, response):
        id = response.meta["id"]
        json_object = json.loads(response.body)
        datas = json_object["data"]["cards"]
        if len(datas) > 0:
        #判断用户是否有数据
         for data in datas:
                 if data["card_type"] == 9:
                    blog = data["mblog"]
                    item = WeiboContentItem()
                    item["id"] = id
                    # item["pub_date"] = blog["created_at"].encode('utf-8')
                    item["pub_date"] = blog["created_at"]
                    # item["text"] = blog["text"].encode('utf-8')
                    item["text"] = blog["text"]
                    picture = []
                    if ("pics" in blog) :
                        pics = blog["pics"]
                        for pic in pics:
                            # picture.append(pic["url"].encode('utf-8'))
                            picture.append(pic["url"])
                            item["pic"] = pics
                    print (item)'''

    # #粉丝解析
    def parse_fans(self, response):
            item = response.meta["item"]
            data_json = json.loads(response.body)
            item["follow"] = data_json["data"]["userInfo"]["follow_count"]
            item["followers"] = data_json["data"]["userInfo"]["followers_count"]
            item["gender"] = data_json["data"]["userInfo"]["gender"]
            fans_scheme = data_json["data"]["fans_scheme"]
            follow_scheme = data_json["data"]["follow_scheme"]
            # self.current_user.remove(item["ID"])
            return item
