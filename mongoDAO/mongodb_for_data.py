import os
import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import binary
load_dotenv()


class MongoDb():

    def __init__(self):
        self.user = os.environ.get('MONGODB_USER')
        self.password = os.environ.get('MONGODB_PASSWORD')
        self.client = None
        self.max_id = 0

    def connection(self):
        self.client = pymongo.MongoClient(
            'mongodb+srv://' + self.user + ':' + self.password +
            '@movies.9gsbi.mongodb.net/<dbname>?retryWrites=true&w=majority')
        return

    def find_max_movie_id(self):
        try:
            collection = self.client['movies']['info']
            max_doc = collection.find_one(sort=[("movie_id", -1)])
            self.max_id = int(max_doc['movie_id'])
        except:
            return


# 如果doc 存在就更新doc，但如果不存在，插入一筆新的doc並且增加primary key: max_id

    def find(self, date, title):
        cursor = self.client['movies']['info'].find({
            "release_date": date,
            "origin_title": title
        })
        return cursor

    def insert(self, doc):
        try:
            movie_id = doc['movie_id']
            self.client['movies']['info'].update({'movie_id': movie_id},
                                                 {'$set': doc})
        except:
            self.max_id += 1
            self.client['movies']['info'].update(doc, {
                '$set': doc,
                '$setOnInsert': {
                    'movie_id': self.max_id
                }
            },
                                                 upsert=True)
        return
