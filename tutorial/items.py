# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import datetime
import re
import redis

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

#from settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
from w3lib.html import remove_tags

from tutorial.models.es_types import ArticleType

from elasticsearch_dsl.connections import connections
es=connections.create_connection(ArticleType._doc_type.using)


redis_cli = redis.StrictRedis(host='172.30.51.102', port=6379,db=0) 

class DmozItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    #url = scrapy.Field()
    #stockcode = scrapy.Field()
    #title = scrapy.Field()
    #resultText = scrapy.Field()
    #source = scrapy.Field()
    #releasetime = scrapy.Field()   
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()    
    
class NewsItem(scrapy.Item): 
    stockcode = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    resultText = scrapy.Field()
    source = scrapy.Field()
    releasetime = scrapy.Field()  
    createtime = scrapy.Field() 
    
class Good(scrapy.Item):
    mall=scrapy.Field()
    rank=scrapy.Field()
    title=scrapy.Field()
    price=scrapy.Field()
    turnover_index=scrapy.Field()
    top_id=scrapy.Field()
    type_id1=scrapy.Field()
    type_id2=scrapy.Field()
    url=scrapy.Field()
    createtime = scrapy.Field() 
    
class GubaItem(scrapy.Item):
    topicId=scrapy.Field()
    clickNum=scrapy.Field()
    replyNum=scrapy.Field()	
    title=scrapy.Field()
    url=scrapy.Field()
    author=scrapy.Field()
    pubDate=scrapy.Field()
    updateDate=scrapy.Field()
    uniqueid=scrapy.Field()
    content=scrapy.Field()
    createtime = scrapy.Field() 
    
class GubaStat(scrapy.Item):
    scode=scrapy.Field()
    page=scrapy.Field()
    createtime = scrapy.Field()    

class GubaProbe(scrapy.Item):
    today=scrapy.Field()
    startdate=scrapy.Field()
    starturl=scrapy.Field()
    pubDate=scrapy.Field()
    topicId=scrapy.Field()
    commenturl=scrapy.Field()
    title=scrapy.Field()
    valid=scrapy.Field()
    createtime = scrapy.Field()     

def add_jobbole(value):
    return value+"-bobby"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value

def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests

class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, create_date, fav_nums, front_image_url, front_image_path,
            praise_nums, comment_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """

        front_image_url = ""
        # content = remove_tags(self["content"])

        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"],
                  fron_image_url, self["front_image_path"], self["praise_nums"], self["comment_nums"],
                  self["tags"], self["content"])
        return insert_sql, params
    
    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.create_date = self["create_date"]
        article.content = remove_tags(self["content"])
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = self["tags"]
        article.meta.id = self["url_object_id"]    
        article.suggest=gen_suggests(ArticleType._doc_type.index, ((article.title,10),(article.tags,7)))
    
        article.save()
        
        redis_cli.incr("jobbole_count")
        
        return 
    