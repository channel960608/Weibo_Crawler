from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
import json
import random
import time
import logging

# from ..items import BasicInfoItem

from ..items import BasicInfoItem
from ..items import WeiboContentItem
from ..items import FansItem
import requests
import random
import re

import importlib,sys
importlib.reload(sys)

logger = logging.getLogger("crawler_logging")
class UserSpider(scrapy.Spider):
    name = 'crawler_all_users'
    start_urls = ['http://m.weibo.cn/']

    start_user = 100000000
    users = set()

    current_user = None

    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 '
        'Mobile/13B143 Safari/601.1]',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/48.0.2564.23 Mobile Safari/537.36'
        ]
    
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
    # login_url = 'https://passport.weibo.cn/signin/login'

    def login(self):
        session = requests.session()
        # username = input('请输入用户名:\n')
        # password = input('请输入密码：\n')
        self.post_data['username'] = "15071300838"
        self.post_data['password'] = "fengqingduo"
        r = session.post(self.login_url, data=self.post_data, headers=self.login_headers)
        if r.status_code != 200:
            raise Exception('Remote server did not response')
        else:
            print("Loging in...............")
            #模拟登录获得cookie填充到下一步请求的header中
            cookiesDic = requests.utils.dict_from_cookiejar(r.cookies)
            loginCookie = ""
            if 'SCF' not in cookiesDic:
                print("Can not get SCF from cookies")
                # raise Exception('Can not get SCF from cookies')
                print("Wait 30 seconds to retry")
                time.sleep(30)
                self.login()
            else:
                loginCookie += "SCF" + ':' + cookiesDic['SCF'] + ';'
                loginCookie += "SUB" + ':' + cookiesDic['SUB'] + ';'
                loginCookie += "SUHB" + ':' + cookiesDic['SUHB'] + ';'
                loginCookie += "SSOLoginState" + ':' + cookiesDic['SSOLoginState'] + ';'
                Cookie = "_T_WM=4ce5b7e0381a4c1cda42834cfa39ec95;%s WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=luicode=20000174&lfid=2302831669879400&fid=1005051712539910&uicode=10000011"%(loginCookie)
                self.basicInfo_headers['Cookie'] = Cookie
                self.basicInfo_headers['User_Agent'] = random.choice(self.user_agents)
                print("Success!")

    def get_users(self):
        users = []
        
        f = open("./data/user_list.txt")
        user_id = f.readlines()
        f.close()
        # random.randint(0, 138)
        index = random.randint(0, len(user_id))
        users.append(user_id[index])
        return user_id[index]


    def start_requests(self):
        self.login()
        id = self.get_users()
        users = ['1867231047\n']

        for id in users:
            # self.current_user = re.sub("\\n", "", id)

            self.current_user = id[:-1]
            # homepage = "https://m.weibo.cn/u/" + "%s"%self.current_user

            random_time = random.random() * 2
            time.sleep(random_time)
            # basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s"%(self.current_user, self.current_user)
            fans_url = "https://m.weibo.cn/api/container/getIndex?uid=%s&luicode=20000174&type=uid&value=%s&containerid=100505%s" % (self.current_user, self.current_user, self.current_user)
            yield scrapy.Request(fans_url, headers = self.basicInfo_headers,callback=self.parse_fans_url, meta={"id":self.current_user})

            

    def start_requests_demo(self):
        self.login()
        # users = self.get_users() 
        users = [5582155304]
        for userid in users:
            # self.current_user = re.sub("\\n", "",userid)
            self.current_user = userid
            # homepage = "https://m.weibo.cn/u/" + "%s"%self.current_user
            #这里最好用随机数
            time.sleep(random.random() * 2)

            basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s"%(self.current_user, self.current_user)
            yield scrapy.Request(basic_info_page, headers = self.basicInfo_headers,callback=self.parse_basicInfo, meta={"id":self.current_user})

            #https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=1669879400&containerid=1076031669879400&page=2

            #weibo_page = "https://m.weibo.cn/api/container/getIndex?from[]=feed&from[]=feed&loc[]=nickname&loc[]=nickname&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&type=uid&value=%010d&containerid=107603%010d&page=1"%(self.start_user, self.start_user)
    def parse_fans_url(self, response):
        json_object = json.loads(response.body)
        isContinue = json_object["ok"] 

        if isContinue == 1:
            fans_scheme = json_object["data"]["fans_scheme"]
            data = str(fans_scheme.split("index?")[1]).replace("fans_intimacy","fans")
            fans_url = "https://m.weibo.cn/api/container/getIndex?"
            fans_url = fans_url + data + "&since_id="
            # print(fans_url)
            index = 1
            next_url = fans_url + str(index)
            yield scrapy.Request(next_url, headers = self.basicInfo_headers,callback=self.get_fans, meta={"fans_url":fans_url, "index":index}, dont_filter = True)
 

        
        pass

        

    
    def parse_basicInfo(self):
        print("parse")
        pass

    def get_fans(self, response):
        # fans_url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_3738004612&luicode=10000011&lfid=1005053738004612&since_id=7"
        index = response.meta["index"] + 1
        fans_url = response.meta["fans_url"] 
        json_object = json.loads(response.body)
        isContinue = json_object["ok"]
        if isContinue == 1:
            for group in json_object["data"]["cards"]:
                if 'card_group' in group and group['card_type'] == 11:
                    for card in group["card_group"]:
                        if "user" in card:
                            user = card["user"]
                            id = user["id"]
                            print(id)
                            print(user)
                            item = FansItem()
                            try:
                                item["id"] = user["id"]
                                item["nickname"] = user["screen_name"]
                                item["profile_image_url"] = user["profile_image_url"]
                                item["profile_url"] = user["profile_url"]
                                if not user["statuses_count"] is None:
                                    item["statuses_count"] = user["statuses_count"]
                                
                                if user["verified"] == True:
                                    item["verified"] =  1
                                else:
                                    item["verified"] =  0
                                # item["verified"] = user["verified"]
                                
                                if not user["verified_type"] is None:
                                    item["verified_type"] = user["verified_type"]    
                                if user["close_blue_v"] is None:
                                    pass
                                elif user["close_blue_v"] == False:
                                    item["close_blue_v"] =  0
                                elif user["close_blue_v"] == True:
                                    item["close_blue_v"] =  1
                                # item["close_blue_v"] = user["close_blue_v"]
                                item["description"] = user["description"]
                                if not user["urank"] is None:
                                    item["urank"] = user["urank"]
                                item["mbtype"] = user["mbtype"]
                                if not user["gender"] is None:
                                    item["gender"] = user["gender"]
                                item["follow_count"] = user["follow_count"]
                                item["followers_count"] = user["followers_count"]
                                item["cover_image_phone"] = user["cover_image_phone"]
                                if not user["desc1"] is None:
                                    item["desc1"] = user["desc1"]
                                if not user["desc2"] is None:
                                    item["desc2"] = user["desc2"]
                                yield item
                            except:
                                logger.err(user)
                                pass
                                
                            
                            
                        else:
                            pass
                else:
                    pass
            # cards = json_object["data"]["cards"][1]
            yield scrapy.Request(fans_url + str(index), headers = self.basicInfo_headers,callback=self.get_fans, meta={"fans_url":fans_url, "index":index}, dont_filter = True)
            
        else:
            pass
                
                # item = BasicInfoItem()
                # item["ID"] = user["id"]
                # item["nickname"] = user["nickname"]
                # item["gender"] = user["gender"]
                # item["follow"] = user["follow_count"]
                # item["followers"] = user["followers_count"]
                # item["nickname"] = user["nickname"]
                # item["nickname"] = user["nickname"]
                # item["nickname"] = user["nickname"]

            


