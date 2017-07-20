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

from tutorial.items import NewsItem
#至简，工具化

class SinaRedisSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""  
    name = 'SinaRedis'  
    redis_key = 'SinaRedis:start_urls'      
    #name = 'sina_spider'
    #allowed_domains = ['sina']
    #start_urls = ['http://money.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sh600031&Page=1']
    
    def __init__(self, *args, **kwargs):  
        # Dynamically define the allowed domains list.  
        #domain = kwargs.pop('domain', '')  
        #self.allowed_domains = filter(None, domain.split(','))  
        super(SinaRedisSpider, self).__init__(*args, **kwargs) 
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
        url=response.url
        code=url[url.rfind('?')+10:url.rfind('?')+16]
        for sel in  response.xpath('//div[@class="datelist"]/ul/a'):
            #标题链接
            
            item = NewsItem()
            #item['stockcode']=self.stockcode[2:]
            item['stockcode']=code
            url = sel.xpath('@href').extract()[0]
            #print("url:",url)
            item['link'] = url
            item['title'] = sel.xpath('text()').extract()[0]
            try:
                yield scrapy.Request(url, callback=self.parse_news_contents, meta={'key':item})
            except Exception as e:
                print("异常发生")
                
            
        #下一页 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[2]/td/div[3]/a
        #for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
        nextlink = response.xpath('//a[text()="下一页"]/@href').extract()
        #print("---------nextlink-----------:",nextlink)
        if nextlink:
            #url = response.urljoin(response.url, href.extract())
            yield scrapy.Request(nextlink[0], callback=self.parse,dont_filter=True)

    #处理新闻详情网页,注意老版本html格式
    def parse_news_contents(self, response):
        is_newpage=response.xpath('//div[@class="wrap-inner"]').extract()
        #is_oldpage=response.xpath('//div[@class="blkContainer"]').extract()
        if is_newpage:
            for sel in response.xpath('//div[@class="wrap-inner"]'):
                #文本内容
                item=response.meta['key'] 
                #print('*************item************:',item)
                #item['title'] = sel.xpath('//h1[@id="artibodyTitle"]/text()').extract()
                #item['resultText'] = sel.xpath('//div[@id="artibody"]/p/text()').extract()
                
                resultText=""
                for p in sel.xpath('//div[@id="artibody"]/p/text()'):
                    resultText=resultText+ p.extract().strip()
                item['resultText']=resultText 
                stringlist= sel.xpath('//span[@class="time-source"]//a/text() | //span[@class="time-source"]/text()').extract()
                #来源和日期，不能处理就放弃处理
                try:
                    if len(stringlist)>1:
                        item["source"]=stringlist[1].strip() #有链接的新闻来源
                        item["releasetime"]=stringlist[0].strip() 
                    else:
                        splitlist=stringlist[0].strip().split(" ") #没有链接的新闻来源
                        item["source"]=splitlist[-1]
                        item["releasetime"]=splitlist[0]  
                except Exception as e:
                    item['source'] = stringlist
                    item['releasetime'] = stringlist
                yield item  
        else:
            for sel in response.xpath('//div[@class="blkContainer"]'):
                #文本内容
                item=response.meta['key'] 
                #item['title'] = sel.xpath('//h1[@id="artibodyTitle"]/text()').extract()
                #item['resultText'] = sel.xpath('//div[@id="artibody"]/p/text()').extract()
        
                resultText=""
                for p in sel.xpath('//div[@id="artibody"]/p/text()'):
                    resultText=resultText+ p.extract().strip()
                item['resultText']=resultText 
                item['source'] = ''.join(sel.xpath('//span[@id="media_name"]/a/text()').extract())
                item['releasetime'] = ''.join(sel.xpath('//span[@id="pub_date"]/text()').extract())
                yield item              
            

             
                   
        
