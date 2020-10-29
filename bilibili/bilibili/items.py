# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # rank_num: 排名, title: 视频名称, author: 作者, aid: 视频号, url: 视频链接, play_num: 播放量, comment_num: 评论数
    rank_num = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    rank_type = scrapy.Field()
    rank_day = scrapy.Field()
    play_num = scrapy.Field()
    comment_num = scrapy.Field()
    coin = scrapy.Field()
    favorite = scrapy.Field()
    like = scrapy.Field()
    aid = scrapy.Field()


class ListItem(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    rank_type = scrapy.Field()
    rank_day = scrapy.Field()
    view = scrapy.Field()
    comment = scrapy.Field()
    follow = scrapy.Field()
    season_id = scrapy.Field()
    coin = scrapy.Field()
    author = scrapy.Field()



