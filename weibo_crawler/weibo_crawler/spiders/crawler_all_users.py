from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
import json
import random
import time
import logging
import datetime
from .WeiboBaseSpider import WeiboBaseSpider

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
class UserSpider(WeiboBaseSpider):
    name = 'crawler_all_users'
    def get_users(self):
        # users = []
        
        f = open("./data/user_list.txt")
        user_id = f.readlines()
        f.close()
        # random.randint(0, 138)
        # index = random.randint(0, len(user_id))
        # for i=0; i< len(user_id); i++:
            # users.append(user_id[i])
        # users.append(user_id[index])
        return user_id


    def start_requests(self):
        self.login()
        users = self.get_users()
        # users = ['1867231047\n']

        for id in users:
            # self.current_user = re.sub("\\n", "", id)

            self.current_user = id[:-1]
            # homepage = "https://m.weibo.cn/u/" + "%s"%self.current_user

            random_time = random.random() * 2
            time.sleep(random_time)
            # basic_info_page = "https://m.weibo.cn/api/container/getIndex?containerid=230283%s_-_INFO&luicode=10000011&lfid=230283%s"%(self.current_user, self.current_user)
            fans_url = "https://m.weibo.cn/api/container/getIndex?uid=%s&luicode=20000174&type=uid&value=%s&containerid=100505%s" % (self.current_user, self.current_user, self.current_user)
            yield scrapy.Request(fans_url, headers = self.basicInfo_headers,callback=self.parse_fans_url, meta={"id":self.current_user})

            

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
            yield scrapy.Request(next_url, headers = self.basicInfo_headers,callback=self.get_fans, meta={"fans_url":fans_url, "index":index})
        
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
                            # id = user["id"]
                            # print(id)
                            # print(user)
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
                                # item["time"] = time.time()
                                now = datetime.datetime.now()
                                now = now.strftime("%Y-%m-%d %H:%M:%S")
                                item["time"] = now
                                yield item
                            except Exception as e:
                                logger.err(e)
                                pass
                                
                            
                            
                        else:
                            pass
                else:
                    pass
            # cards = json_object["data"]["cards"][1]
            yield scrapy.Request(fans_url + str(index), headers = self.basicInfo_headers,callback=self.get_fans, meta={"fans_url":fans_url, "index":index})
            
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

            


