# Scrapy settings for bilibili project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from .spiders.proxy_spider import ProxySpider

BOT_NAME = 'bilibili'

SPIDER_MODULES = ['bilibili.spiders']
NEWSPIDER_MODULE = 'bilibili.spiders'

MONGODB_HOST = 'host'
MONGODB_PORT = 'port'
MONGODB_DBNAME = 'bilibili'
MONGODB_DOCNAME = 'rank'

RID_URL = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid={}&type={}'
LIST_URL = 'https://api.bilibili.com/pgc/season/rank/web/list?day=3&season_type={}'
NEW_LIST_URL = 'https://api.bilibili.com/pgc/web/rank/list?day=3&season_type={}'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bilibili (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'user-agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/83.0.4103.61 '
                 'Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'bilibili.middlewares.BilibiliSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'bilibili.middlewares.UserAgentMiddleware': 543,
    'bilibili.middlewares.ProxyMiddleware': 544,
    'bilibili.middlewares.RetryMiddleware': None,
    'bilibili.middlewares.LocalRetryMiddleware': 549,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bilibili.pipelines.RankPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# scrapy_redis setting
# Enable scheduling storing requests queue in redis.
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

# whether cleanup redis queues
SCHEDULER_PERSIST = False

# Ensure all spiders share same duplicates filter through redis
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Redis host and port
REDIS_HOST = 'host'
REDIS_PORT = 6379

# retry settings
# Enable and configure retry
RETRY_ENABLE = True
RETRY_TIMES = 5
HTTPERROR_ALLOWED_CODE = [412]


# Proxy Spider
proxy = ProxySpider()
proxy.get_proxy_list()
