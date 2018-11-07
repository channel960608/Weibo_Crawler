# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchByKeywordItem(scrapy.Item):
    # define the fields for your item here like:
	pub_date = scrapy.Field()
	text= scrapy.Field()
	pic = scrapy.Field()


class WeiboCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickname = scrapy.Field()

    pass

class WeiboContentItem(scrapy.Item):
	userid = scrapy.Field()
	id = scrapy.Field()
	pub_date = scrapy.Field()
	text= scrapy.Field()
	pic = scrapy.Field()


class BasicInfoItem(scrapy.Item):
	ID = scrapy.Field()	
	nickname = scrapy.Field()		#昵称
	gender = scrapy.Field()			#性别
	age = scrapy.Field()			#年龄
	tags = scrapy.Field()			#标签
	brief_intro = scrapy.Field()	#简介
	verify = scrapy.Field()			#微博认证
	location = scrapy.Field()		#所在地
	level = scrapy.Field()			#等级
	signup_date = scrapy.Field()	#注册时间
	credit = scrapy.Field()			#阳光信用
	company = scrapy.Field()		#公司
	school = scrapy.Field()			#学校
	blog = scrapy.Field() 			#博客
	follow = scrapy.Field()			#关注人数
	followers = scrapy.Field()		#粉丝人数

class FansItem(scrapy.Item):
	id = scrapy.Field()	
	nickname = scrapy.Field()		
	profile_image_url = scrapy.Field()			
	profile_url = scrapy.Field()			
	statuses_count = scrapy.Field()			
	verified = scrapy.Field()	
	verified_type = scrapy.Field()		
	close_blue_v = scrapy.Field()		
	description = scrapy.Field()			
	gender = scrapy.Field()
	urank = scrapy.Field()			
	mbtype = scrapy.Field()		
	followers_count = scrapy.Field()			
	follow_count = scrapy.Field() 			
	cover_image_phone = scrapy.Field()			
	desc1 = scrapy.Field()		
	desc2 = scrapy.Field()
	time = scrapy.Field()

	def get(self, key):
		if key in self.keys():
			return self[key]
		else:
			return None		

