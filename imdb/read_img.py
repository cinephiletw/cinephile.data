import os
import json
import pymongo
import requests
from ast import literal_eval
from dotenv import load_dotenv
from pymongo import MongoClient
from gridfs import *
load_dotenv()
tmdb_api_key = os.environ.get('TMDB_API_KEY')
user = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PASSWORD")


# 連mongoDB
def connection():
    client = pymongo.MongoClient(
        "mongodb+srv://" + user + ":" + password +
        "@movies.9gsbi.mongodb.net/<dbname>?retryWrites=true&w=majority")
    return client


def main():
    mongo_client = connection()
    fs = GridFS(mongo_client.popular_movies_img, collection='backdrop')
    for grid_out in fs.find():
        data = grid_out.read()
        outf = open('./img/' + 'backdrop' + '.jpg', 'wb')
        outf.write(data)
        outf.close()


main()
