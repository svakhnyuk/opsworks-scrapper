import target.model
from configparser import ConfigParser

class TargetPipeline(object):

    store_mongo_db = True
    storage_config = {}

    def __init__(self):
        parser = ConfigParser()
        parser.read('scrapy.cfg')

        if 'mongo' in self.storage_config and self.storage_config['mongo'].lower() == "false":
            self.store_mongo_db = False

    def open_spider(self, spider):
        if self.store_mongo_db:
            self.mongo_db = target.model.Model_mongo_db()

    def close_spider(self, spider):
        if self.store_mongo_db:
            self.mongo_db.close()

    def process_item(self, item, spider):
        """
        Save deals in the database.
        This method is called for every item pipeline component.
        """
        if item:
            if self.store_mongo_db is True:
               self.mongo_db.insert(collection_name=self.mongo_db.collection, data=dict(item))
        return item

