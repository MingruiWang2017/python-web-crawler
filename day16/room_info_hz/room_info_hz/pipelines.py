# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

class RoomInfoHzPipeline:
    def __init__(self, host, port, db_name, username, password, docname):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.docname = docname
        client = pymongo.MongoClient(self.host, self.port, username=self.username, password=self.password)

        db = client[db_name]
        self.collection = db[self.docname]

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get("MONGODB_HOST"),
                   settings.get("MONGODB_PORT"),
                   settings.get("MONGODB_NAME"),
                   settings.get("MONGODB_USERNAME"),
                   settings.get("MONGODB_PASSWORD"),
                   settings.get("MONGODB_DOCNAME"))

    def process_item(self, item, spider):
        room = dict(item)
        self.collection.insert(room)
        return item
