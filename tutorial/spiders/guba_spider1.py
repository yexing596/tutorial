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
from tutorial.items import GubaItem
#至简，工具化

class GubaRedisSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""  
    name = 'GubaRedis1'  
    redis_key = 'GubaRedis1:start_urls'      
    #name = 'sina_spider'
    #allowed_domains = ['sina']
    #start_urls = ['http://money.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600031&Page=1']
    
    def __init__(self, *args, **kwargs):  
        # Dynamically define the allowed domains list.  
        #domain = kwargs.pop('domain', '')  
        #self.allowed_domains = filter(None, domain.split(','))  
        super(GubaRedisSpider, self).__init__(*args, **kwargs) 
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
        #global earlydate
        #earlydate='2017-06-01'
        for sel in  response.xpath('//div[@class="articleh"]'):
            #标题链接text()
            #for sel in sel_m.xpath('span'):
            item = GubaItem()
            
            try:
                #if sel.xpath('span[@class="l3"]/em').extract()==[]:
                tempValue = sel.xpath('span[@class="l3"]/a/@href').extract()[0].strip('/')
                #print("tempValue:",tempValue)
                url='http://guba.eastmoney.com/'+tempValue
                item['topicId']=str(tempValue.split(',')[1])
                item['clickNum']=sel.xpath('span[@class="l1"]/text()').extract()[0]
                item['replyNum']=sel.xpath('span[@class="l2"]/text()').extract()[0]
                item['title']=sel.xpath('span[@class="l3"]/a/@title').extract()[0]
                item['url']=url
                try:
                    item['author']=sel.xpath('span[@class="l4"]/span[@class="gray"]/text()').extract()[0]
                except  Exception as e: 
                    item['author']=sel.xpath('span[@class="l4"]/a/text()').extract()[0]
                #
                
                #item['pubDate'] = sel.xpath('span[@class="l6"]/text()').extract()[0]
                #item['updateDate']=  sel.xpath('span[@class="l5"]/text()').extract()[0]
                item['uniqueid']=str(tempValue.split(',')[1])+str(tempValue.split(',')[2].replace(".html",''))
    
                yield scrapy.Request(url, callback=self.parse_news_contents, meta={'key':item})
                    
                #else:continue
            except Exception as e:
                pass
                #print("异常发生")                
            
            
        #下一页 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[2]/td/div[3]/a
        #for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        '''
        try:
            #print('$$$$$$$$$$$$$$$$$earlydate:',earlydate)
            #input()
            pager=response.xpath('//span/@data-pager').extract()[0].split(',')[2].split('|')
            nextpage=int(pager[-1])+1
            if int(pager[-3])/int(pager[-2]) > int(pager[-1]) :#and earlydate>='2017-04-30':
                nextlink=response.url[0:39]+'_%i.html'%nextpage
                
                
                yield scrapy.Request(nextlink, callback=self.parse,dont_filter=True)
        except Exception as e:
            pass            
        '''
           
    def parse_news_contents(self, response):
        #global earlydate
        item=response.meta['key'] 
        
        pattern=re.compile(r'\d{4}-\d{2}-\d{2} +\d{2}:\d{2}:\d{2}')
        item['pubDate'] =pattern.search(response.xpath('//div[@class="zwfbtime"]/text()').extract()[0]).group(0)
        
        #if item['pubDate'] <earlydate:
        #    earlydate=item['pubDate']
        #print("earlydate:",earlydate)
        
        try:
            item['updateDate']= pattern.search(response.xpath('//div[@class="zwlitime"]/text()').extract()[-1]).group(0)
        except Exception as e:
            item['updateDate']=item['pubDate']
        item['content']=response.xpath('//div[@class="stockcodec"]/text()').extract()[0].strip()
        
        yield item  
        
        
        