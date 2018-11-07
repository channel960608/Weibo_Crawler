    # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import MySQLdb
# import MySQLdb.cursors

# MySQL-python does not currently support Python 3, thus we replace it with PyMySQL
import pymysql
import pymysql.cursors

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured

from scrapy.http import Request
from scrapy.exceptions import DropItem
# from scrapy import log
import logging
from .items import BasicInfoItem, WeiboContentItem, FansItem
import time
import datetime
import json
import codecs
import random

logger = logging.getLogger('mycustomlogger')

class WeiboCrawlerPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # cls.password = settings['WEIBO_PASSWORD']
        # cls.username = settings['WEIBO_USERNAME'] 
 
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            # cursorclass = MySQLdb.cursors.DictCursor,
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode= True,
        )
        # dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        dbpool = adbapi.ConnectionPool('pymysql', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item, spider)
        query.addErrback(self.handle_error, item, spider)
        # return query

    def _conditional_insert(self, cursor, item, spider):
        try:
            if spider.name == "user_info_spider":
            # 判断id是否已经存在
            # conn.execute("""select id from user where id = "%s";"""%(item["ID"])
                
                sql = "select id from user where id = '%s'" % (item["ID"])
                cursor.execute(sql)
                results = cursor.fetchone()
                if results:
                    cursor.execute(
                        """update user set nickname = "%s", gender = "%s", location = "%s",
                        brief_intro = "%s", follow = "%s", followers = "%s" where id = "%s";"""%
                        (item["nickname"],
                        item["gender"],
                        item["location"],
                        item["brief_intro"],
                        item["follow"],
                        item["followers"],
                        item["ID"]
                        ))
                else:
                    cursor.execute(
                        """insert into user (id, nickname, gender, location, brief_intro, follow, followers)
                        values ("%s", "%s", "%s", "%s", "%s", "%s", "%s");"""%
                        (item["ID"],
                        item["nickname"],
                        item["gender"],
                        item["location"],
                        item["brief_intro"],
                        item["follow"],
                        item["followers"]
                        ))
                    # conn.execute(
                    # """insert into user (id, nickname, gender, location, brief_intro, follow, followers)
                    # values ("%s", "%s", "%s", "%s", "%s", "%s", "%s");"""%
                    # (item["ID"],
                    #  item["nickname"],
                    #  item["gender"],
                    #  item["location"],
                    #  item["brief_intro"],
                    #  item["follow"],
                    #  item["followers"]
                    # ))

                if "verify" in item:
                    cursor.execute("update user set verify = '%s' where id = '%s';"%(item["verify"], item["ID"]))
                if "tags" in item:
                    cursor.execute("update user set tags = '%s' where id = '%s';"%(item["tags"], item["ID"]))
                if "level" in item:
                    cursor.execute("update user set level = '%s' where id = '%s';"%(item["level"], item["ID"]))
                if "company" in item:
                    cursor.execute("update user set company = '%s' where id = '%s';"%(item["company"], item["ID"]))
                if "school" in item:
                    cursor.execute("update user set school = '%s' where id = '%s';"%(item["school"], item["ID"]))
                if "blog" in item:
                    cursor.execute("update user set blog = '%s' where id = '%s';"%(item["blog"], item["ID"]))
            elif spider.name == "weibo_content_spider":
                cursor.execute(
                """insert into weibo_content (userid, id, pub_date, text) values ('%s', '%s', '%s', '%s');"""%
                    (item["userid"],
                    item["id"],
                    item["pub_date"],
                    item["text"]
                    ))
                if "pic" in item:
                    cursor.execute('update weibo_content set pic = "%s" where id = "%s";'%(item["pic"], item["id"]))
            elif spider.name == "crawler_all_users":
                sql = 'insert into fans (id, nickname, profile_image_url, profile_url, statuses_count, verified, verified_type, close_blue_v, description, gender, urank, mbtype, followers_count, follow_count, cover_image_phone, desc1, desc2, time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)'
                cursor.execute(sql, (item.get("id"),
                    item.get("nickname"),
                    item.get("profile_image_url"),
                    item.get("profile_url"),
                    item.get("statuses_count"),
                    item.get("verified"),
                    item.get("verified_type"),
                    item.get("close_blue_v"),
                    item.get("description"),
                    item.get("gender"),
                    item.get("urank"),
                    item.get("mbtype"),
                    item.get("followers_count"),
                    item.get("follow_count"),
                    item.get("cover_image_phone"),
                    item.get("desc1"),
                    item.get("desc2"),
                    item.get("time")
                    ))
                # conn.execute
                # """insert into fans (id, nickname, profile_image_url, profile_url, statuses_count, verified, verified_type, close_blue_v, description, gender, urank, mbtype, followers_count, follow_count, cover_image_phone, desc1, desc2, time) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s');"""%
                #     (item.get("id"),
                #     item.get("nickname"),
                #     item.get("profile_image_url"),
                #     item.get("profile_url"),
                #     item.get("statuses_count"),
                #     item.get("verified"),
                #     item.get("verified_type"),
                #     item.get("close_blue_v"),
                #     item.get("description"),
                #     item.get("gender"),
                #     item.get("urank"),
                #     item.get("mbtype"),
                #     item.get("followers_count"),
                #     item.get("follow_count"),
                #     item.get("cover_image_phone"),
                #     item.get("desc1"),
                #     item.get("desc2"),
                #     item.get("time")
                #     ))
            # random_time = random.random() * 2
            # time.sleep(random_time)
        except Exception as e:
            if e.args[0] == 1062:
                logger.info(e)
        finally:
            # if conn:
            #     conn.close()
            pass
                
    def handle_error(self, e, item, spider):
        # log.err(e)
        # logger.error(e)
        print(item)
        logger.error(e)
    
    # def close_spider(self, spider):
        
    #     self.dbpool.close()
        


class WeiboJsonPipeline(object):
    def __init__(self):
        #self.dbpool = dbpool
        self.info_file = codecs.open('/data/info_result.json', 'wb', 'utf-8')
        self.content_file = codecs.open('/data/content_result.json', 'wb', 'utf-8')
        self.searchByKeyWord = codecs.open('/data/searchByKeyWord_content.json', 'wb', 'utf-8')

    def process_item(self, item, spider):
        if spider.name == "user_info_spider":
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.info_file.write(line)
            return item
        elif spider.name == "weibo_content_spider":
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.content_file.write(line)
            return item
        elif spider.name == "search_by_keyword":
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.searchByKeyWord.write(line)
            return item

    def close_spider(self,spider):
        self.info_file.close()
        self.content_file.close()
        self.searchByKeyWord.close()
