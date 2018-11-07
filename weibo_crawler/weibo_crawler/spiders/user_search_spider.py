# -*- coding: utf-8 -*-
import scrapy
import json
import re
import codecs

import importlib,sys
importlib.reload(sys)
from .WeiboBaseSpider import WeiboBaseSpider
# sys.setdefaultencoding('utf8')

class UserSearchSpiderSpider(WeiboBaseSpider):
    name = "user_search_spider"
    allowed_domains = ["m.weibo.cn"]
    
    #搜索筛选前几名，默认为1，即只选取搜索到的第一个用户
    limit = 1
    user_count = 0
    #在这个数组里面放入要爬取的用户
    user_names = ['爱我所爱_过好现在', '七色瓜', 'tt', 'mengtwei', 'DanicaReus', 'Tough_xzy', 'w', '香蕉你个芭拉yu-', '哈哈哈', '十月的阿朱', 'ana', '。', '墨默520', '续汉冕', '叶子-恋', '圆妮今天写作业了嘛', '欧益晞XD', '玉多多多多多', '中文数字-', 'aha', '独爱神话', 'xiahualiang', '不常用微博', '木易杨', '啊，不可以', '一个很胖的胖子嘞', 'haha', '飞驰的熊猫', 'cgbcharm', '沈飞13183', 'jessie_时间煮雨我煮泡面', 'HaHa', '凡人之凡路', 'IAMXO', '齐子尧Charles', '吴鸣超', '芭拉焦', 'Z-little倩', '王但是', '加麦', '花果山荔枝大王', 'broccolibaby', '瘦了就不用经常买衣服了', 'Mr-Dynamite-Zhang', 'de ffa y', '1.0', '奥黛尔0226', '还是爱吃煎饼果子', 'Wym的wb', '蘑菇菌想假装沉迷学习', '衣锦夜行的燕公子！', '俄罗斯的哥斯拉', 'Cassie想要每一天都是纪念日', '比biu', '陌猫灵℃', '没有微博', '春暖花开', '关关戼戼', 'tangbin', '鄭白告文', '一棵小树', 'wang', '小鸡腿子啊', '刘君仪Joyee', '智障青年养乐多', '豆腐干傻乎乎阿萨德', '小卷紫拉', '湾崽崽', '枭哭在路上', '拦春', '没有微博', 'Ryzor', 'LTL_cn', 'today_fighting', '七桑', 'Sophhhhhhia', '忘记了', '爱吃橘子的我CCC', '哈哈笑出翔', '采桑子南']
    # user_names = []
    page = 1
    

    def start_requests(self):
        with codecs.open('./68个用户/crawl_user.txt', 'r',encoding="utf8") as f:
            users = f.readlines()
            for user in users:
                user = re.sub("\\n", "",user)
                self.user_names.append(user)
            print (self.user_names)
            for user in self.user_names:
                self.current_user = user
                search_page = "https://m.weibo.cn/api/container/getIndex?type=user&queryVal=%s&from=feed&luicode=10000011&title=%s&containerid=100103type%%3D3%%26q%%3D%s&page=1"%(user, user, user)
                print(search_page)
                yield scrapy.Request(search_page, callback=self.parse)


    def parse(self, response):
        hasNext = True
        user = self.current_user
        json_object = json.loads(response.body)
        datas = json_object["data"]["cards"]
        if len(datas) > 1:
            users_data = datas[1]["card_group"]
            for user_data in users_data:
                user_id = user_data["user"]["id"]
                user_name = user_data["user"]["screen_name"]
                self.user_count += 1
                f = open('crawl_user.txt','a+')
                f.write(str(user_id) + '\n')
                f.close()
                f1 = open('name_id.txt', 'a+')
                f1.write(str(user_name) + '\t' + str(user_id) + '\n')
                f1.close()

                if self.user_count >= self.limit:
                    break
        else:
            #停止爬取下一页
            hasNext = False

        if self.user_count < self.limit and len(datas) > 0 and hasNext:
            self.page += 1
            search_page = "https://m.weibo.cn/api/container/getIndex?type=user&queryVal=%s&from=feed&luicode=10000011&title=%s&containerid=100103type=3&q=%s&page=%s"%(user, user, user, self.page)
            yield scrapy.Request(search_page, self.parse)
        else:
            self.page = 1
            self.user_count = 0
