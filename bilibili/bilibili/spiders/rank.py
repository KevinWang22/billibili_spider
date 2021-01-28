import scrapy
import time
import re
import json
from ..items import BilibiliItem, ListItem
from scrapy_redis.spiders import RedisSpider


class RankSpider(RedisSpider):
    name = 'rank'
    redis_key = 'rank:start_urls'
    allowed_domains = ['bilibili.com']
    rank_type_dict = {
        '0': '全站',
        '168': '国创相关',
        '1': '动画',
        '3': '音乐',
        '129': '舞蹈',
        '4': '游戏',
        '36': '知识',
        '188': '数码',
        '160': '生活',
        '211': '美食',
        '119': '鬼畜',
        '155': '时尚',
        '5': '娱乐',
        '181': '影视',
        '原创': '0',
        '新人': '0',
    }
    list_rank_types = {
        '1': '番剧',  # list
        '4': '国产动画',  # list
        '3': '纪录片',  # list
        '2': '电影',  # list
        '5': '电视剧',  # list
    }

    def make_requests_from_url(self, url):

        if 'origin' in url:
            return scrapy.Request(url=url, callback=self.parse, meta={'rank_type': '原创'})
        elif 'rookie' in url:
            return scrapy.Request(url=url, callback=self.parse, meta={'rank_type': '新人'})
        elif 'pgc/season' in url:
            rank_type = self.list_rank_types[url.split('season_type=')[-1]]
            return scrapy.Request(url=url, callback=self.parse_list, meta={'rank_type': rank_type})
        elif 'pgc/web' in url:
            # print('番剧url', url)
            return scrapy.Request(url=url, callback=self.parse_list, meta={'rank_type': '番剧'})
        else:
            rank_type = self.rank_type_dict[url.split('rid=')[1].split('&')[0]]
            return scrapy.Request(url=url, callback=self.parse, meta={'rank_type': rank_type})

    def parse(self, response):

        rank_type = response.meta['rank_type']
        rank_item_list = response.json()['data']['list']
        base_url = 'https://www.bilibili.com/video/'
        for rank_item in rank_item_list:
            title = rank_item['title']
            rank = rank_item['score']
            aid = rank_item['aid']
            bvid = rank_item['bvid']
            author = rank_item['owner']['name']
            view = rank_item['stat']['view']  # 观看数
            comment = rank_item['stat']['danmaku']  # 弹幕数
            favour = rank_item['stat']['favorite']  # 收藏数
            like = rank_item['stat']['like']  # 点赞数
            coin = rank_item['stat']['coin']  # 投币数
            url = base_url + bvid
            rank_day = time.strftime('%Y-%m-%d', time.localtime())

            item = BilibiliItem()
            item['title'] = title
            item['rank_num'] = rank
            item['author'] = author
            item['url'] = url
            item['rank_type'] = rank_type
            item['rank_day'] = rank_day
            item['play_num'] = view
            item['comment_num'] = comment
            item['coin'] = coin
            item['favorite'] = favour
            item['like'] = like
            item['aid'] = aid
            # print(item)
            yield item

    def parse_list(self, response):

        detail_header = self.settings['DEFAULT_REQUEST_HEADERS']
        rank_type = response.meta['rank_type']
        if rank_type == '番剧':
            # print(response.json())
            rank_item_list = response.json()['result']['list']
        else:
            rank_item_list = response.json()['data']['list']

        for rank_item in rank_item_list:
            title = rank_item['title']
            url = rank_item['url']
            rank = rank_item['rank']
            season_id = rank_item['season_id']
            view = rank_item['stat']['view']
            comment = rank_item['stat']['danmaku']
            follow = rank_item['stat']['follow']

            item = ListItem()
            item['title'] = title
            item['rank'] = rank
            item['url'] = url
            item['season_id'] = season_id
            item['view'] = view
            item['comment'] = comment
            item['follow'] = follow
            item['rank_type'] = rank_type
            item['rank_day'] = time.strftime('%Y-%m-%d', time.localtime())
            # print(item)

            yield scrapy.Request(url=url, headers=detail_header,
                                 callback=self.parse_detail, meta={'list_item': item})

    def parse_detail(self, response):

        item = response.meta['list_item']

        author = response.xpath('//div[@class="up-info clearfix"]/a/span/text()').extract_first()
        item['author'] = author

        init_state_text = re.findall(r'__INITIAL_STATE__=(.*?);', response.text)[0]
        # print(init_state)
        init_state = json.loads(init_state_text)
        coin = init_state['mediaInfo']['stat']['coins']

        item['coin'] = coin

        # print(item)
        yield item






