# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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

    
   
