import re
import datetime
import requests
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import DanmakuItem


class DanmuSpider(RedisSpider):
    name = 'danmu'
    allowed_domains = ['bilibili.com']
    # start_urls = ['http://bilibili.com/']
    custom_settings = {
        'LOG_FILE': './bilibili/logs/%slog.log' % name
    }

    def make_requests_from_url(self, url):
        aid = re.findall(r'pid=(.*?)&', url, re.S)[0]
        cid = re.findall(r'oid=(.*?)&', url, re.S)[0]

        return scrapy.Request(url=url, callback=self.parse, meta={'aid': aid,
                                                                  'cid': cid, })

    def parse(self, response):
        aid = response.meta['aid']
        cid = response.meta['cid']
        # 返回的是二进制流数据
        encrypt_data = response.body
        # 调用node.js的解密方法，返回dict数据，格式{'elems':[{danmu},{danmu},]}
        decrypt_data = requests.post(url=self.settings['DECRYPT_URL'],
                                     data={'encrypt_data': list(encrypt_data)}).json()

        danmu_items = DanmakuItem()
        danmu_items['aid'] = aid
        danmu_items['cid'] = cid
        danmu_items['danmaku'] = decrypt_data['elems']
        danmu_items['update_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield danmu_items


