豆瓣爬虫

1. crawl_list.py: 爬取http://movie.douban.com/top250?format=text 页面上的电影排名信息。

2. crawl_detail.py: 爬取http://movie.douban.com/top250?format=text 页面上电影的详细信息。
包括电影基本信息、评分、简介和评论。


## 依赖

    1. BeautifulSoup


## 数据存放格式

doc/top250.txt文件存放爬取信息，存放格式如下：

排名|电影名|详情页面url|评分|评分人数|导演|演员|上映年份|地区|简评

少数几部电影没有简评。

doc/detail/目录下存放crawl_detail.py爬取的信息。每部电影一个文件。数据存放格式：

排名|电影名|年份|导演|编剧|主演|类型|地区|语言|上映日期|片长|又名|IMDB链接

[空行]

总评分|评分人数|5星评分百分比|4星|3星|2星|1星

[空行]

tag1|tag2|tag3|...

[空行]

电影简介

[空行]

奖项类别：奖项1|奖项2|奖项3|...

[空行]

评论数

评论人|评论日期|评分|评语|认为该评论有用的人数

ATTENTION: 评论人字段可能为空。
