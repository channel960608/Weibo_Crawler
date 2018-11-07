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
from scrapy.exceptions import NotConfigured
import importlib,sys
importlib.reload(sys)
from scrapy.utils.project import get_project_settings
# sys.setdefaultencoding('utf8')

class WeiboBaseSpider(scrapy.Spider):

    def __init__(self):
        settings = get_project_settings()
        self.post_data['username'] = settings.get('WEIBO_USERNAME')
        self.post_data['password'] = settings.get('WEIBO_PASSWORD')

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
        # self.post_data['username'] = "15071300838"
        # self.post_data['password'] = "fengqingduo"
        # self.post_data['username'] = self
        


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
