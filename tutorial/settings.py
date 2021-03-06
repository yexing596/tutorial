# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

#DUPEFILTER_CLASS='scrapy.dupefilters.RFPDupeFilter'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#JOBDIR='where'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tutorial.middlewares.TutorialSpiderMiddleware': 543,
#}

#SPIDER_MIDDLEWARES = {
    #'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tutorial.middlewares.MyCustomDownloaderMiddleware': 543,
#}


#RETRY_ENABLED=True
# Retry many times since proxies often fail
#RETRY_TIMES = 3
# Retry on most error codes since proxies fail for different reasons
#RETRY_HTTP_CODES = [500,502,503,504,400,408]


#DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 200,
    #'scrapy_splash.SplashCookiesMiddleware': 723,
    #'scrapy_splash.SplashMiddleware': 725,
    #'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'tutorial.pipelines.CleanPipeline': 200,
    'tutorial.pipelines.CheckPipeline':298,
    'tutorial.pipelines.EncodingPipeline':299,    
    'tutorial.pipelines.MongoPipeline': 300,
    #'tutorial.pipelines.ElasticsearchPipeline':301
    #'tutorial.pipelines.TutorialPipeline': 300,
    #'scrapy_redis.pipelines.RedisPipeline': 400,
}



MONGO_URI = "172.30.51.102"
MONGO_PORT = 27017
MONGO_DATABASE = 'SinaNews'
#MONGO_COLLECTION = 'StocksNews'
MONGO_UID='ETLUser'
MONGO_PWD='1e7Lg80mWaz04nI3ke9z'

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#SPLASH_URL = 'http://192.168.99.100:8050'
#DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
#HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

#'''
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True #False
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
#REDIS_URL = None # 一般情况可以省去
REDIS_HOST = '172.30.51.102' # 也可以根据情况改成 localhost
REDIS_PORT = 6379
#'''