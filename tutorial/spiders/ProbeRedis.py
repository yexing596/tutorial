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
from tutorial.items import GubaItem,GubaProbe
import time,datetime
#至简，工具化

class GubaRedisSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""  
    name = 'ProbeRedis'  
    redis_key = 'ProbeRedis:start_urls'      
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
        
        item = GubaProbe()
        today=datetime.date.today()    #今天为参考日
        start_url=response.url
        item['today']=today.strftime('%Y-%m-%d')   
        item['startdate']=(today-datetime.timedelta(days=4)).strftime('%Y-%m-%d') #需要从该日期开始读取，爬取到的数据的发布必须小于这个日期
        item['starturl']=start_url
        
        try:
            sel = response.xpath('//div[@class="articleh"]')[-1]
            try:
                tempValue = sel.xpath('span[@class="l3"]/a/@href').extract()[0].strip('/')
                url='http://guba.eastmoney.com/'+tempValue
                #item['pubDate'] 在comment里面去获取
                #topicId与其他爬虫与区别，这里要获取文章所在页面，不是股票
                item['topicId']=item['starturl'][31:37]
                item['commenturl']=url
                item['title']=sel.xpath('span[@class="l3"]/a/@title').extract()[0]
                item['valid']=1                

                yield scrapy.Request(url, callback=self.parse_news_contents, meta={'key':item},dont_filter=True)
                 
            except Exception as e:
                pass            
        except Exception as e:
            
            item['pubDate']=item['startdate'] 
            item['topicId']=start_url[31:37]
            item['commenturl']=''
            item['title']=''
            item['valid']=0
            yield item 
                     
            
            
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
        
        pattern=re.compile(r'\d{4}-\d{2}-\d{2}')
        item['pubDate'] =pattern.search(response.xpath('//div[@class="zwfbtime"]/text()').extract()[0]).group(0)
        
        if item['pubDate']<item['startdate']:
            yield item  
        else:
            url=item['starturl']
            page=int(url[40:].rstrip(".html"))
            
            nextlink=url[0:40]+str(page+5)+".html"
            
            yield scrapy.Request(nextlink, callback=self.parse,dont_filter=True)
        
        
        
        
        