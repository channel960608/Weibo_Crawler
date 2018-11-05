# WeiboCrawler
新浪微博爬虫
主体使用Scrapy框架完成  
目的是通过用户关注以及被关注的名单，实现微博用户的爬取  
获取用户之后就可以实现全站的微博数据爬取
目前正准备通过Scrapy+Redis框架实现分布式的爬取以及存储

#### 2018年11月5日更新  
基于之前项目已经实现的功能进行了拓展，已经实现的功能如下：  
- 根据用户名搜索用户的id __user_search_spider__  
- 根据用户的id，爬取其发布的微博 __weibo_content_spider__  
- 根据用户的id，爬取用户的信息 __user_info_spider__  
为了绕开验证以及简化爬取方式，爬取了移动端的微博(m.weibo.cn)  
已经拓展完成的功能包括：  
- 存储方式从json文件修改为数据库存储  
- 添加了根据用户id获取粉丝列表的功能
基本实现爬取微博的各个功能，包括爬取粉丝列表，爬取用户微博内容
为了获取微博全站用关注以及被关注情况，实现了爬取用户的粉丝列表的功能


程序使用：（macOS环境）
1. 修改配置
	settings.py文件中有关于数据库的配置，本机使用的是MySQL
	数据库结构在根目录中
	要爬取的用户名在/WeiboCrawler/weibo_crawler/weibo_crawler/spiders/user_search_spider.py中的users_name修改
	首先通过微博搜索找到用户，limit字段表示取搜索结果的前几位
	将搜索到的用户id存储在crawl_user.txt文件中，每次修改要爬取的用户名或者limit后需要删除该文件并重新运行user_search_spider

2. 运行
	爬取逻辑是先爬取用户名对应的id
	然后通过fans爬虫爬取个人信息
	然后通过content爬虫爬取每个用户的微博内容

	进入根目录
	爬取id：scrapy crawl user_search_spider
	爬取内容：scrapy crawl weibo_content_spider
	爬取个人信息：scrapy crawl user_info_spider


#### 2018年9月11日更新
加入根据关键词爬取微博的模块（与之前模块不冲突，无视其他模块即可）

设置：  
先在search_by_keyword.py中
设置一个微博用户名密码用以登陆
(login函数里，self.post_data['username'] = "xxxxx"，self.post_data['password'] = "xxxxx")
再设置keywords
(start_requests函数里，key_words =['一带一路'])

运行：  
先激活虚拟环境（`WeiboCrawler/weibo_crawler/crawler_env`）  
进入根目录（`WeiboCrawler/weibo_crawler/`）  
爬取微博：__scrapy crawl search_by_keyword__
最后数据存在`searchByKeyWord_content.json`文件中

#### 2018年10月30日更新  
转变了item存储方式，将json文件存储修改为数据库存储
数据库配置: __/weibo_crawler/weibo_crawler/settings.py__  
```
MYSQL_HOST = ''  
MYSQL_DBNAME = ''  
MYSQL_USER = ''  
MYSQL_PASSWD = ''
```    
##### 注意：  
只修改了输出数据的存储方式，在爬取用户微博数据时，遍历的用户id是通过txt文档的方式输入的（和之前一样）






