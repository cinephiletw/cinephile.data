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
    data = mongo_collection.find({"movie_id": {
        "$gt": 79
    }}, {
        "movie_id": 1,
        "image_path": 1,
        "poster_path": 1
    })
    data_img = []
    for d in data:
        print(d['movie_id'])
        break
        try:
            index = 0
            for image in d['image_path']:
                image_img = requests.get(image, timeout=10).content
                folder = './../api/public/images/backdrop/image_path_' + str(
                    d['movie_id'])
                if not os.path.exists(folder):
                    os.mkdir(folder)
                with open(
                        './../api/public/images/backdrop/image_path_' +
                        str(d['movie_id']) + '/' + str(d['movie_id']) + '_' +
                        str(index) + '.jpg', 'wb') as f:
                    f.write(image_img)
                index += 1
        except:
            print(str(d['movie_id']) + 'do not have image')
    #  try:
    #      poster_img = requests.get(d["poster_path"], timeout=10).content
    #      with open(
    #              './../api/public/images/poster/poster_path_' +
    #              str(d['movie_id']) + '.jpg', 'wb') as f:
    #          f.write(poster_img)
    #  except:
    #      print('fail')


main()
