import os
import json
import pymongo
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from gridfs import *
load_dotenv()
user = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PASSWORD")


def main():
    client = pymongo.MongoClient(
        "mongodb+srv://" + user + ":" + password +
        "@movies.9gsbi.mongodb.net/<dbname>?retryWrites=true&w=majority")

    mongo_collection = client['movies']['info']
    data = mongo_collection.find({}, {
        "id": 1,
        "image_path": 1,
        "poster_path": 1
    })
    data_img = []
    for d in data:
        for image in d['image_path']:
            image_img = requests.get(image, timeout=10).content
            with open(
                    './../api/images/' + str(d['id']) + '/' + str(d['id']) +
                    '.jpg', 'wb') as f:
                f.write(backdrop_img)
        poster_img = requests.get(d["poster_path"], timeout=10).content
        with open('./../api/images/poster_path_' + str(d['id']) + '.jpg',
                  'wb') as f:
            f.write(poster_img)
        break


main()
