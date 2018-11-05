#! /bin/bash
cd /Users/channel/work/Projects/WeiboCrawler/weibo_crawler
scrapy crawl user_search_spider
scrapy crawl user_info_spider
scrapy crawl weibo_content_spider
rm -rf /Users/channel/work/Projects/WeiboCrawler/weibo_crawler/crawl_user.txt