import scrapy
import time
import re
import json
import random
from ..items import BilibiliItem, ListItem, PageItem, EpItem
from scrapy_redis.spiders import RedisSpider


class RankSpider(RedisSpider):
    name = 'rank'
    redis_key = 'rank:start_urls'
    allowed_domains = ['bilibili.com']
    custom_settings = {
        'LOG_FILE': './logs/%slog%s.log' % (name, time.strftime('%y%m%d-%H-%M', time.localtime()))
    }
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
        """
        普通up主上传的视频的解析方法，如果视频没有分集，可以直接解析完全部数据，如果视频有分集的话，需要再请求一个detail接口，
        在detail中取每个分集的信息
        :param response: 返回包
        :return: 没有分集的时候，返回BilibiliItem对象； 有分集的时候，返回一个Request对象
        """
        rank_type = response.meta['rank_type']
        rank_date = time.strftime('%Y-%m-%d', time.localtime())
        rank_item_list = response.json()['data']['list']
        base_url = 'https://www.bilibili.com/video/'
        # 每一个item对应一个视频，如果视频没有分集，那直接取完所有数据，提交item就行了，如果有分集，就需要再发请求获取每集数据
        for rank_item in rank_item_list:
            item = BilibiliItem()
            item['bvid'] = rank_item['bvid']
            item['title'] = rank_item['title']
            item['author'] = rank_item['owner']['name']
            item['author_mid'] = rank_item['owner']['mid']
            item['aid'] = rank_item['aid']
            item['score'] = rank_item['score']
            item['description'] = rank_item['desc']
            item['rank_type'] = rank_type
            item['rank_date'] = rank_date
            item['url'] = base_url + rank_item['bvid']
            # 观看数
            item['view'] = rank_item['stat']['view']
            # 弹幕数
            item['danmakus'] = rank_item['stat']['danmaku']
            # 投币数
            item['coin'] = rank_item['stat']['coin']
            # 收藏数
            item['favorite'] = rank_item['stat']['favorite']
            # 点赞数
            item['like'] = rank_item['stat']['like']
            if rank_item['videos'] == 1:
                item['pages'] = [{'aid': rank_item['aid'],
                                  'cid': rank_item['cid'],
                                  'page': 1,
                                  'part': item['title'],
                                  }]
            else:
                item['pages'] = []

                detail_url = self.settings.get('DETAIL_URL').format(bvid=item['bvid'], aid=item['aid'])
                yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'rank_date': rank_date,
                                                                                       'rank_type': rank_type})

            yield item

    def parse_detail(self, response):
        """
        解析正常up主上传的视频中的分集信息
        :param response: 请求返回的包
        :return item: BilibiliItem对象
        """
        rank_date = response.meta['rank_date']
        rank_type = response.meta['rank_type']
        detail_infos = response.json()['data']
        pages = detail_infos['View']['pages']
        item = PageItem()
        for page in pages:
            item['rank_date'] = rank_date
            item['rank_type'] = rank_type
            item['aid'] = detail_infos['View']['aid']
            item['cid'] = page['cid']
            item['page'] = page['page']
            item['part'] = page['part']

            yield item

    def parse_list(self, response):
        """
        解析番剧、电视剧这些B站自己上传的视频信息，因为这些都是有分集的，所以在取完整部剧的信息后，需要调用每个分集的info接口，获取分集信息
        :param response: make_request_from_url返回的包
        :return: Request对象，请求播放页数据，从播放页的html文件中提取信息
        """
        rank_type = response.meta['rank_type']
        if rank_type == '番剧':
            # 番剧和其他类型返回的数据的key不一样
            # print(response.json())
            rank_item_list = response.json()['result']['list']
        else:
            rank_item_list = response.json()['data']['list']

        for rank_item in rank_item_list:

            item = ListItem()
            item['rank_type'] = rank_type
            item['rank_date'] = time.strftime('%Y-%m-%d', time.localtime())
            item['season_id'] = rank_item['season_id']
            item['title'] = rank_item['title']
            item['url'] = rank_item['url']
            item['rank_score'] = rank_item['pts']
            item['badge'] = rank_item['badge']
            item['total_stat'] = {
                'danmakus': rank_item['stat']['danmaku'],
                'follow': rank_item['stat']['follow'],
                'series_follow': rank_item['stat']['series_follow'],
                'view': rank_item['stat']['view'],
            }
            # print(item)

            yield scrapy.Request(url=item['url'], callback=self.parse_list_detail, meta={'list_item': item})

    def parse_list_detail(self, response):
        """
        提取剧集播放页的信息，对于每一集，都要单独请求一个分集的info接口，读取分集的stat数据
        :param response: parse_list请求返回的包
        :return: Request对象，调用info接口
        """
        item = response.meta['list_item']
        init_state_text = re.findall(r'__INITIAL_STATE__=(.*?);', response.text)[0]
        # print(init_state)
        init_state = json.loads(init_state_text)
        media_info = init_state['mediaInfo']
        item['total_stat'].update({
            'coins': media_info['stat']['coins'],
            'reply': media_info['stat']['reply'],
            'share': media_info['stat']['share'],
        })
        item['id'] = media_info['id']
        item['series'] = media_info['series']
        item['evaluate'] = media_info['evaluate']
        item['up_info'] = {
            'mid': media_info['upInfo']['mid'],
            'name': media_info['upInfo']['name'],
        }
        item['rating'] = {
            'score': media_info['rating']['score'],
            'count': media_info['rating']['count'],
        }
        item['ep_list'] = []
        yield item

        # 每集的基础信息
        ep_list = init_state['epList']
        for ep in ep_list:
            ep_item = EpItem()
            ep_item['rank_date'] = item['rank_date']
            ep_item['rank_type'] = item['rank_type']
            ep_item['season_id'] = item['season_id']
            ep_item['id'] = ep['id']
            ep_item['aid'] = ep['aid']
            ep_item['bvid'] = ep['bvid']
            ep_item['cid'] = ep['cid']
            ep_item['title'] = ep['title']
            ep_item['title_format'] = ep['titleFormat']
            ep_item['long_title'] = ep['longTitle']
            ep_info_url = self.settings.get('EP_INFO_URL').format(ep_id=ep['id'])
            headers = {
                'origin': 'https://www.bilibili.com',
                'referer': item['url'],
            }
            yield scrapy.Request(url=ep_info_url, callback=self.parse_ep_info, headers=headers, meta={'item': ep_item})

    def parse_ep_info(self, response):
        """
        解析每集的stat数据
        :param response: parse_list_detail返回的包
        :return: ListItem对象
        """
        item = response.meta['item']
        ep_data = response.json()['data']
        ep_stat = ep_data['stat']
        item['stat'] = ep_stat

        yield item






