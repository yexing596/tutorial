#from scrapy_redis.spiders import RedisSpider

#class MySpider(RedisSpider):  
    #"""Spider that reads urls from redis queue (myspider:start_urls)."""  
    #name = 'myspider_redis'  
    #redis_key = 'myspider:start_urls'  
  
    #def __init__(self, *args, **kwargs):  
        ## Dynamically define the allowed domains list.  
        #domain = kwargs.pop('domain', '')  
        #self.allowed_domains = filter(None, domain.split(','))  
        #super(MySpider, self).__init__(*args, **kwargs)  
  
    #def parse(self, response):  
        #return {  
            #'name': response.css('title::text').extract_first(),  
            #'url': response.url,  
        #} 
    
    
# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
#from static.items import GubaItem
from tutorial.items import GubaStat
#至简，工具化

class GubaMonitorSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""  
    name = 'GubaMonitor'  
    redis_key = 'GubaMonitor:start_urls'      
    #name = 'sina_spider'
    #allowed_domains = ['sina']
    #start_urls = ['http://money.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600031&Page=1']
    
    def __init__(self, *args, **kwargs):  
        # Dynamically define the allowed domains list.  
        #domain = kwargs.pop('domain', '')  
        #self.allowed_domains = filter(None, domain.split(','))  
        super(GubaMonitorSpider, self).__init__(*args, **kwargs) 
        #self.stockcode=stockcode
            
    '''        
    def __init__(self, stockcode='sh600031', *args, **kwargs):
        super(SinaSpiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://money.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol={0}&Page=1'.format(stockcode)]
        self.stockcode=stockcode
    '''    
    '''   
    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    '''
    def parse(self, response):
        #找到具体的新闻列表网站

        item = GubaStat()
        try:
            item['scode']=response.url[31:37] 
            pager=response.xpath('//span/@data-pager').extract()[0].split(',')[2].split('|')
            item['page']=pager[-3]
            yield item 
        except Exception as e:
            pass
            #print("异常发生")                
            
       

           
        
        