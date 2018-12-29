# WeiboCrawler
新浪微博爬虫
主体使用Scrapy框架完成  
目的是通过用户关注以及被关注的名单，实现微博用户的爬取  
获取用户之后就可以实现全站的微博数据爬取
目前正准备通过Scrapy+Redis框架实现分布式的爬取以及存储

### Requirements  
- Python 3.*  
    需要自行安装  
- Scrapy 1.5  
    安装python之后，可以通过 __pip__ 安装
    __pip install Scrapy__  
- requests  
    __pip install Requests__  

#### 2018年11月7日更新  
- 对爬虫项目中代码冗余的问题进行处理，借助继承的思想，抽象出了基础爬虫类 __WeiboBaseSpider__  ，登录功能以及相关的一些变量被提取到父类中     
- 将微博登录账号信息提取到setting.py中  

#### 2018年11月22日更新  
- 添加了指定用户所关注的用户列表的爬虫，爬虫名字为 __crawl_followings__  
- 防止ip被禁用，增加了下载时延为0.25s


#### 2018年11月5日更新  
基于之前项目已经实现的功能进行了拓展，已经实现的功能如下：  
- 根据用户名搜索用户的id __user_search_spider__  
- 根据用户的id，爬取其发布的微博 __weibo_content_spider__  
- 根据用户的id，爬取用户的信息 __user_info_spider__  
- 根据关键词搜索微博内容 __search_by_keyword__ (是否添加了数据库存储？)     

为了绕开验证以及简化爬取方式，爬取了移动端的微博(m.weibo.cn)  
拓展完成的功能包括：  
- 存储方式从json文件修改为数据库存储,后期将会将json文件存储设置为可选项  
- 添加了根据用户id获取粉丝列表的功能  

基本实现爬取微博的各个功能，包括爬取粉丝列表，爬取用户微博内容
为了获取微博全站用关注以及被关注情况，实现了爬取用户的粉丝列表的功能  
爬取用户关系图之后，可以利用可视化工具来表现微博用户关注情况关系图  
目前需要完成的工作：  
- 将输入参数从硬解码修改为软解码，将输入提出到外部文件  
- 数据库连接未关闭，会出现问题  
- 目前环境为macOS，需要补充windows以及linux环境下的配置方式


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

	进入/WeiboCrawler_distribute/weibo_crawler/下
	爬取id：scrapy crawl user_search_spider  
	爬取内容：scrapy crawl weibo_content_spider  
	爬取个人信息：scrapy crawl user_info_spider  
	搜索关键字微博：scrapy crawl search_by_keyword  
	爬取用户粉丝： scrapy crawl crawler_all_users   

windows下(需要进行测试)：  
	运行：  
	先激活虚拟环境（`WeiboCrawler/weibo_crawler/crawler_env`） 
	进入根目录（`WeiboCrawler/weibo_crawler/`）  
	爬取微博：__scrapy crawl search_by_keyword__
	最后数据存在`searchByKeyWord_content.json`文件中








