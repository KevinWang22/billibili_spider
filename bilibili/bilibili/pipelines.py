# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from itemadapter import ItemAdapter


class RankPipeline:

    def __init__(self, db_host, db_post, db_name, db_doc):
        self.db_host = db_host
        self.db_post = db_post
        self.db_name = db_name
        self.db_doc = db_doc

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('MONGODB_HOST'), crawler.settings.get('MONGODB_POST'),
                   crawler.settings.get('MONGODB_DBNAME'), crawler.settings.get('MONGODB_DOCNAME'))

    def open_spider(self, spider):
        self.db_client = MongoClient(host=self.db_host, port=self.db_post)
        self.db = self.db_client[self.db_name]
        self.b_post = self.db[self.db_doc]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.b_post.insert(ItemAdapter(item).asdict())
        return item
