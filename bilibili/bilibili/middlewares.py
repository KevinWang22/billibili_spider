# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
import requests
from random import choice
from redis import StrictRedis
from scrapy import signals
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.retry import RetryMiddleware, response_status_message
from scrapy.settings.default_settings import RETRY_HTTP_CODES

redis_client = StrictRedis()
proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=30&type=2&pro=&city=0&yys=0&port=11&pack=139612&ts=1&ys=0' \
            '&cs=0&lb=1&sb=0&pb=45&mr=2&regions='


class BilibiliSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware:

    def __init__(self, redis_host, redis_port):
        self.redis_client = StrictRedis(host=redis_host, port=redis_port)

    @classmethod
    def from_crawler(cls, crawler):

        return cls(redis_host=crawler.settings['REDIS_HOST'], redis_port=crawler.settings['REDIS_PORT'])

    def process_request(self, request, spider):
        """给请求增加代理"""
        if not request.meta.get('proxy', False):
            if not self.redis_client.exists(spider.settings['REDIS_PROXY_KEY']):
                get_proxies(spider)
            using_proxy = self.redis_client.lpop(spider.settings['REDIS_PROXY_KEY']).decode()
            if '/' in using_proxy:
                using_proxy = using_proxy.replace('/', '')
            spider.logger.info('using_proxy: %s' % using_proxy)
            request.meta['proxy'] = using_proxy

    def process_response(self, request, response, spider):
        """回收有效的代理"""
        if response.status not in RETRY_HTTP_CODES:
            self.redis_client.rpush(spider.settings['REDIS_PROXY_KEY'], request.meta['proxy'])

        return response


class UserAgentMiddleware:

    def process_request(self, request, spider):

        request.headers['user-agent'] = choice(spider.settings['USER_AGENTS_LIST'])


class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            request.meta['proxy'] = None
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider)

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            request.meta['proxy'] = None
            return self._retry(request, exception, spider)


def get_proxies(spider):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36',
        'Host': 'webapi.http.zhimacangku.com'
    }
    resp = requests.get(url=proxy_url, headers=headers).json()
    if resp['success']:
        for ip_info in resp['data']:
            ip = ip_info['ip']
            port = ip_info['port']
            full_proxy = ip + ':' + str(port)
            # expire_time = ip_info['expire_time']
            redis_client.rpush(spider.settings['REDIS_PROXY_KEY'], full_proxy)
    else:
        spider.crawler.engine.close_spider(spider, '代理ip获取失败，原因: ' + resp['msg'])
