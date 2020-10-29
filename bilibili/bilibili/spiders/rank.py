import scrapy
import time
import re
import json
from ..items import BilibiliItem, ListItem


class RankSpider(scrapy.Spider):
    name = 'rank'
    allowed_domains = ['bilibili.com']
    rank_type_dict = {
        '全站': '0',
        '番剧': '1',
        '国产动画': '4',
        '国创相关': '168',
        '纪录片': '3',
        '动画': '1',
        '音乐': '3',
        '舞蹈': '129',
        '游戏': '4',
        '知识': '36',
        '数码': '188',
        '生活': '160',
        '美食': '211',
        '鬼畜': '119',
        '时尚': '155',
        '娱乐': '5',
        '影视': '181',
        '电影': '2',
        '电视剧': '5',
        '原创': '0',
        '新人': '0',
    }
    list_rank_types = [
        '番剧',  # list
        '国产动画',  # list
        '纪录片',  # list
        '电影',  # list
        '电视剧',  # list
    ]

    def start_requests(self):
        headers = self.settings['DEFAULT_REQUEST_HEADERS']
        for rank_type, rank_id in self.rank_type_dict.items():
            if rank_type == '原创':
                url = self.settings['RID_URL'].format(rank_id, 'origin')
                yield scrapy.Request(url=url, headers=headers,
                                     callback=self.parse, meta={'rank_type': rank_type})
            elif rank_type == '新人':
                url = self.settings['RID_URL'].format(rank_id, 'rookie')
                yield scrapy.Request(url=url, headers=headers,
                                     callback=self.parse, meta={'rank_type': rank_type})
            elif rank_type in self.list_rank_types:
                if rank_type != '番剧':
                    url = self.settings['LIST_URL'].format(rank_id)
                    yield scrapy.Request(url=url, headers=headers,
                                         callback=self.parse_list, meta={'rank_type': rank_type})
                else:
                    url = self.settings['NEW_LIST_URL'].format(rank_id)
                    # print('番剧url', url)
                    yield scrapy.Request(url=url, headers=headers,
                                         callback=self.parse_list, meta={'rank_type': rank_type})
            else:
                url = self.settings['RID_URL'].format(rank_id, 'all')
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, meta={'rank_type': rank_type})

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
            view = rank_item['stat']['view']    # 观看数
            comment = rank_item['stat']['danmaku']  # 弹幕数
            favour = rank_item['stat']['favorite']  # 收藏数
            like = rank_item['stat']['like']    # 点赞数
            coin = rank_item['stat']['coin']    # 投币数
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






