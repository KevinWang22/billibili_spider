# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from redis import StrictRedis
from pymongo import MongoClient
from bson import ObjectId
from itemadapter import ItemAdapter
from twisted.internet import defer, reactor
from .items import BilibiliItem, ListItem, DanmakuItem, PageItem, EpItem
from scrapy.utils.log import logger


class RankPipeline:

    def __init__(self, db_host, db_post, db_name, db_doc, redis_host, redis_port):
        self.db_host = db_host
        self.db_post = db_post
        self.db_name = db_name
        self.db_doc = db_doc
        self.redis_host = redis_host
        self.redis_port = redis_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGODB_HOST'), crawler.settings.get('MONGODB_POST'),
                   crawler.settings.get('MONGODB_DBNAME'), crawler.settings.get('MONGODB_DOCNAME'),
                   crawler.settings.get('REDIS_HOST'), crawler.settings.get('REDIS_PORT'))

    def open_spider(self, spider):
        self.db_client = MongoClient(host=self.db_host, port=self.db_post)
        self.db = self.db_client[self.db_name]
        self.b_post = self.db[self.db_doc]
        self.redis_client = StrictRedis(host=self.redis_host, port=self.redis_port)

    def close_spider(self, spider):
        self.db_client.close()
        self.redis_client.close()

    def process_item(self, item, spider):
        """
        处理spider传过来的item，当item是BilibiliItem或者ListItem的时候，则在mongodb中插入这个item，
        并构造弹幕的url，传给弹幕爬虫的key
        :param item: spider传过来的item实例
        :param spider: spider
        :return: item
        """
        if isinstance(item, (BilibiliItem, ListItem)):
            # logger.info(item)
            self.b_post.insert_one(ItemAdapter(item).asdict())
            # 插入后构造一个弹幕的url，并写到redis中，弹幕爬虫启动
            # if isinstance(item, BilibiliItem):
                # 如果item是BIlibiliItem的实例，说明是普通Up主上传的视频，分集信息存在item的pages里
                # pages = item['pages']
            # else:
                # 是B站上传的视频，分集信息存在item的ep_list里
                # pages = item['ep_list']

            # for page in pages:
                # 构造每一个分集的danmu_url，并把url插入到redis的list中，以供弹幕爬虫调用
                # danmu_url = spider.settings['DANMU_URL'].format(oid=page['cid'], pid=page['aid'])
                # self.redis_client.rpush(spider.settings.get('REDIS_DANMAKU_KEY'), danmu_url)
        elif isinstance(item, PageItem):
            # logger.info(item)
            rank_date = item.pop('rank_date')
            rank_type = item.pop('rank_type')
            self.b_post.update_one({'aid': item['aid'], 'rank_date': rank_date, 'rank_type': rank_type},
                                   {'$push': {'pages': ItemAdapter(item).asdict()}})
        elif isinstance(item, EpItem):
            rank_date = item.pop('rank_date')
            rank_type = item.pop('rank_type')
            self.b_post.update_one({'season_id': item['season_id'], 'rank_date': rank_date, 'rank_type': rank_type},
                                   {'$push': {'ep_list': ItemAdapter(item).asdict()}})

    def _insert(self, item, out):
        if isinstance(item, (BilibiliItem, ListItem)):
            self.b_post.insert(ItemAdapter(item).asdict())
            # 插入后构造一个弹幕的url，并写到redis中，弹幕爬虫启动
            # if isinstance(item, BilibiliItem):
                # 如果item是BIlibiliItem的实例，说明是普通Up主上传的视频，分集信息存在item的pages里
                # pages = item['pages']
            # else:
                # 是B站上传的视频，分集信息存在item的ep_list里
                # pages = item['ep_list']

            # for page in pages:
                # 构造每一个分集的danmu_url，并把url插入到redis的list中，以供弹幕爬虫调用
                # danmu_url = spider.settings['DANMU_URL'].format(oid=page['cid'], pid=page['aid'])
                # self.redis_client.rpush(spider.settings.get('REDIS_DANMAKU_KEY'), danmu_url)
        elif isinstance(item, PageItem):
            logger.info('_insert ' + item)
            rank_date = ItemAdapter(item).pop('rank_date')
            rank_type = item.pop('rank_type')
            self.b_post.update_many({'aid': item['aid'], 'rank_date': rank_date, 'rank_type': rank_type},
                                    {'$push': {'pages': ItemAdapter(item).asdict()}})
        elif isinstance(item, EpItem):
            rank_date = item.pop('rank_date')
            rank_type = item.pop('rank_type')
            self.b_post.update_many({'season_id': item['season_id'], 'rank_date': rank_date, 'rank_type': rank_type},
                                    {'$push': {'ep_list': ItemAdapter(item).asdict()}})
        reactor.callFromThread(out.callback, item)


class DanmakuPipeline:

    def __init__(self, db_host, db_port, db_name, db_doc):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_doc = db_doc
        self.db_client = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGODB_HOST'), crawler.settings.get('MONGODB_PORT'),
                   crawler.settings.get('MONGODB_DBNAME'), crawler.settings.get('MONGODB_DOCNAME'))

    def open_spider(self, spider):
        self.db_client = MongoClient(host=self.db_host, port=self.db_port)
        self.db = self.db_client[self.db_name]
        self.doc = self.db[self.db_doc]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        """
        当item是DanmakuItem的实例时，把item中的弹幕数据更新到mongodb中去
        :param item: spider传入的item实例
        :param spider: spider
        :return: item
        """
        if isinstance(item, DanmakuItem):
            match_items = self.doc.find({'aid': item['aid'], 'rank_date': item['rank_date']})
            for match_item in match_items:
                _id = match_item['_id']
                if 'pages' in match_item:
                    for idx, page in enumerate(match_item['pages']):
                        if page['cid'] == item['cid']:
                            self.doc.update_one({'_id': ObjectId(_id)},
                                                {
                                                    '$set': {'pages.' + str(idx) + '.danmaku': item}
                                                })
                            break

                elif 'ep_list' in match_item:
                    for idx, ep in enumerate(match_item['ep_list']):
                        if ep['cid'] == item['cid']:
                            self.doc.update_one({'_id': _id},
                                                {
                                                    '$set': {'ep_list.' + str(idx) + '.danmaku': item}
                                                })
                            break

        return item
