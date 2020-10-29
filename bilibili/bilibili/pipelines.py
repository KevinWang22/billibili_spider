# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings


class RankPipeline:
    def __init__(self):
        settings = get_project_settings()
        db_name = settings['MONGODB_DBNAME']
        db_client = MongoClient()
        db = db_client[db_name]
        doc_name = settings['MONGODB_DOCNAME']
        self.b_post = db[doc_name]

    def process_item(self, item, spider):
        b_info = dict(item)
        self.b_post.insert(b_info)
        return item
