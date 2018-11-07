# Record of Project Process
#### 11.7.2018  
完成情况    
- 基本功能实现，目前输入为txt文件，输出为数据库  
- 需要重新设计数据库关系  
- 是否需要修改为MongoDB    

遇到问题  
- 爬取速度太快导致请求403 
    - 先更换为 `Scrapy-Redis` 框架  
    - 添加微博账号，增加cookie池
    - 请求添加速度限制
