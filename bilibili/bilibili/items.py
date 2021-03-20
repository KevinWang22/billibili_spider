# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 正常up主上传的视频item，如果一个视频里有分集，则存每个分集的内容
    # rank_num: 排名, title: 视频名称, author: 作者, aid: 视频号, url: 视频链接, play_num: 播放量, danmaku_num: 弹幕数
    title = scrapy.Field()
    author = scrapy.Field()
    author_mid = scrapy.Field()
    url = scrapy.Field()
    rank_type = scrapy.Field()
    rank_date = scrapy.Field()
    view = scrapy.Field()
    danmakus = scrapy.Field()
    coin = scrapy.Field()
    favorite = scrapy.Field()
    like = scrapy.Field()
    aid = scrapy.Field()
    description = scrapy.Field()
    score = scrapy.Field()
    bvid = scrapy.Field()
    pages = scrapy.Field()


class ListItem(scrapy.Item):

    rank_type = scrapy.Field()
    rank_date = scrapy.Field()
    season_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    # 排行榜得分
    rank_score = scrapy.Field()
    badge = scrapy.Field()
    # 整部剧的评分情况，结构如下:
    # 'total_stat': {
    #         'danmakus': int,
    #         // 追番
    #         'follow': int,
    #         // 系列追番
    #         'serires_follow':int,
    #         'view': int,
    #         // __initial_state__里的
    #         'coins': int,
    #         'reply': int,
    #         'share': int,
    #     }
    total_stat = scrapy.Field()
    id = scrapy.Field()
    series = scrapy.Field()
    evaluate = scrapy.Field()
    # up主的信息
    # 'up_info': {
    #         'mid': '',
    #         'name': '',
    #     }
    up_info = scrapy.Field()
    # 整部剧的评分情况
    # 'rating': {
    #         'score': int,
    #         'count': int,
    #     }
    rating = scrapy.Field()
    # 分集列表
    # 'ep_list': [
    #         {
    #             'id': ep_id,
    #             'aid': '',
    #             'bvid': '',
    #             'cid': '',
    #             'title': '',
    #             'title_format': '',
    #             'long_title': '',
    #             'stat': {
    #                 'coin': int,
    #                 'danmakus': int,
    #                 'like': int,
    #                 'view': int,
    #                 'reply': '',
    #             },
    #             // 弹幕
    #             'danmaku': list,
    #         }]
    ep_list = scrapy.Field()


class PageItem(scrapy.Item):
    rank_date = scrapy.Field()
    rank_type = scrapy.Field()
    aid = scrapy.Field()
    cid = scrapy.Field()
    page = scrapy.Field()
    part = scrapy.Field()


class EpItem(scrapy.Item):
    rank_date = scrapy.Field()
    rank_type = scrapy.Field()
    season_id = scrapy.Field()
    id = scrapy.Field()
    aid = scrapy.Field()
    bvid = scrapy.Field()
    cid = scrapy.Field()
    title = scrapy.Field()
    title_format = scrapy.Field()
    long_title = scrapy.Field()
    stat = scrapy.Field()


class DanmakuItem(scrapy.Item):
    aid = scrapy.Field()
    cid = scrapy.Field()
    danmaku = scrapy.Field()
    update_date = scrapy.Field()



