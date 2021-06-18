import pymongo

from configparser import ConfigParser

parser = ConfigParser()
parser.read('scrapy.cfg')

mongoClient = {}
if parser.has_section('mongod'):
    items = parser.items('mongod')
    for item in items:
        mongoClient[item[0]] = item[1]

class Model_mongo_db(object):
    """
    Model is class to handle and save data to DB
    """

    def __init__(self):
        MdbURI = "mongodb://"
        if 'database' in mongoClient:
            self.db_name = mongoClient['database']
        if 'collection' in mongoClient:
            self.collection = mongoClient['collection']
        if 'user' in mongoClient:
            MdbURI += mongoClient['user']
        if 'password' in mongoClient:
            MdbURI += ":" + mongoClient['password'] + "@"
        if 'host' in mongoClient:
            MdbURI += mongoClient['host']
        if 'port' in mongoClient:
            MdbURI += ":" + mongoClient['port']
        if 'user' in mongoClient and 'password' in mongoClient:
            MdbURI += "/tracking?authSource=admin"
        self.client = pymongo.MongoClient(MdbURI)
        self.db = self.client[self.db_name]

    def close(self):
        self.client.close()

    def insert(self,collection_name, data):
        self.db[collection_name].insert(data)

    def update(self, collection_name, id, data):
        self.db[collection_name].update({"_id": id}, data)

    def get_first_item(self, collection_name, key, value):
        res = self.db[collection_name].find({key: value})
        if res.count() > 0:
            return res[0]
        else:
            return None

    def create_db(self):
        pass

    def create_collection(self):
        pass

