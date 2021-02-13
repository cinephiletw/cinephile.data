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
        "movie_id": 1,
        "image_path": 1,
        "poster_path": 1
    })
    data_img = []
    for d in data:
        try:
            for i, image in enumerate(d['image_path']):
                file_image = './../api/public/images/backdrop/image_path_' + str(
                    d['movie_id']) + '/' + str(
                        d['movie_id']) + '_' + str(i) + '.jpg'
                if not os.path.exists(file_image):
                    image_img = requests.get(image, timeout=10).content
                    createFolder('./../api/public/images/backdrop/image_path_' +
                                 str(d['movie_id']) + '/')
                    with open(file_image, 'wb') as f:
                        f.write(image_img)
                    print('back' + str(d['movie_id']) + '_' + str(i) + ' OK')
                else:
                    print('back' + str(d['movie_id']) + '_' + str(i) +
                          ' exists')
                    continue
        except TypeError:
            print('back' + str(d['movie_id']) + ' None')
            pass
        try:
            file_poster = './../api/public/images/poster/poster_path_' + str(
                d['movie_id']) + '.jpg'
            if not os.path.exists(file_poster):
                poster_img = requests.get(d["poster_path"], timeout=10).content
                with open(file_poster, 'wb') as f:
                    f.write(poster_img)
                print('poster' + str(d['movie_id']) + ' OK')
            else:
                print('poster' + str(d['movie_id']) + ' exists')
        except TypeError:
            print('poster' + str(d['movie_id']) + ' None')
            pass


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
