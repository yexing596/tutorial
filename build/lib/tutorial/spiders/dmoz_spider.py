import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "http://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    #def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
            #f.write(response.body)
            
    def parse(self, response):
        for sel in  response.xpath('//div[@class="title-and-desc"]'):
            item=DmozItem()
            item['title'] = sel.xpath('a/div[@class="site-title"]/text()').extract()#.strip()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('div/text()').extract()#.strip()
            #print(title,link,desc)
            yield item