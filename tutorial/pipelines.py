# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
import datetime
import time

import importlib,sys
importlib.reload(sys)
#sys.setdefaultencoding('utf8')

from scrapy.exceptions import DropItem

from tutorial.items import Good,NewsItem,DmozItem
from tutorial.models.es_types import ArticleType
from w3lib.html import remove_tags

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item


class CheckPipeline(object):
    def process_item(self,item,spider):
        if spider.name == 'taobao_spider': #if isinstance(item, Good):
            for key in item:
                if item[key]==None:
                    raise DropItem('%s is missing %s' % (item,key))
        
        return item

class EncodingPipeline(object):
    def process_item(self,item,spider):
        if spider.name == 'taobao_spider':
            for key in item:
                item[key]=item[key].encode('utf-8')
        return item

'''
class CleanPipeline(object):
    def process_item(self, item, spider):
        try:
            if len(item["source"])>1:
                item["source"]=item["source"][1].strip()
                item["releasetime"]=item["releasetime"][0].strip()
            else:
                splitlist=item["source"][0].strip().split(" ")
                item["source"]=splitlist[-1]
                item["releasetime"]=splitlist[0]
            return item
        except Exception as e:
            return item
'''        

class MongoPipeline(object):
    #collection_name = 'StocksNews'
    mongo_collection={'sina_spider':'StocksNews','splash_demo':'TaoBao','SinaRedis':'StocksNews','GubaRedis':'Guba','GubaRedis1':'Guba_copy','GubaRedis2':'Guba','GubaMonitor':'GubaMonitor','ProbeRedis':'ProbeRedis'}

    def __init__(self, mongo_uri, mongo_db,mongo_uid,mongo_pwd):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_uid = mongo_uid
        self.mongo_pwd = mongo_pwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_uid=crawler.settings.get('MONGO_UID'),
            mongo_pwd=crawler.settings.get('MONGO_PWD')    
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.client[self.mongo_db].authenticate(self.mongo_uid,self.mongo_pwd)
        #if self.client:
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        #item["CreateTime"]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if spider.name == 'sina_spider':
            item["createtime"]=datetime.datetime.now()
            self.db[self.mongo_collection[spider.name]].update({'link': item['link']}, {'$set': dict(item)}, True)
        elif spider.name == 'SinaRedis':
            item["createtime"]=datetime.datetime.now()
            self.db[self.mongo_collection[spider.name]].update({'link': item['link']}, {'$set': dict(item)}, True)        
        elif spider.name == 'splash_demo':
            item["createtime"]=datetime.datetime.now()
            self.db[self.mongo_collection[spider.name]].update({'title': item['title']}, {'$set': dict(item)}, True)            
        elif spider.name == 'GubaRedis':
            item["createtime"]=datetime.datetime.now()
            item["clickNum"]=int(item["clickNum"])
            item["replyNum"]=int(item["replyNum"])
            '''
            self.db[self.mongo_collection[spider.name]].update({'uniqueid': item['uniqueid']}, {'$set': dict(item)}, True)   
            '''
            
            self.db[self.mongo_collection[spider.name]].insert(dict(item))
        elif spider.name == 'GubaRedis1':
            item["createtime"]=datetime.datetime.now()
            item["clickNum"]=int(item["clickNum"])
            item["replyNum"]=int(item["replyNum"])

        
            self.db[self.mongo_collection[spider.name]].insert(dict(item))  
        elif spider.name == 'GubaRedis2':
            item["createtime"]=datetime.datetime.now()
            item["clickNum"]=int(item["clickNum"])
            item["replyNum"]=int(item["replyNum"])
            
            self.db[self.mongo_collection[spider.name]].update({'uniqueid': item['uniqueid']}, {'$set': dict(item)}, True)   
            
        
            #self.db[self.mongo_collection[spider.name]].insert(dict(item))        
        elif spider.name == 'GubaMonitor':
            item["createtime"]=datetime.datetime.now()
            item["page"]=int(item["page"])        
            self.db[self.mongo_collection[spider.name]].insert(dict(item))
        elif spider.name == 'ProbeRedis':
            item["createtime"]=datetime.datetime.now()
            item["valid"]=int(item["valid"])
            self.db[self.mongo_collection[spider.name]].insert(dict(item))            
        return item
    

class ElasticsearchPipeline(object):
    
    def process_item(self,item,spider):
        item.save_to_es()
        return item