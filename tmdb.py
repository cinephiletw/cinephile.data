import os
import json
import pymongo
import requests
from ast import literal_eval
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import binary
load_dotenv()
tmdb_api_key = os.environ.get('TMDB_API_KEY')
user = os.environ.get("MONGODB_USER")
password = os.environ.get("MONGODB_PASSWORD")


# tmdb api 連接方式
def set_tmdb(base_url, page):
    url = base_url + tmdb_api_key
    tmdb_params = {'language': 'zh-TW', 'page': page}
    req = requests.get(url, params=tmdb_params)
    return req


# 獲取熱門電影
def popular():
    pop_req = set_tmdb("https://api.themoviedb.org/3/movie/popular?api_key=", 2)
    pop_id = pop_req.text.replace("false", "False")
    pop_id = eval(pop_id)
    pop_id = pop_id['results']
    id_list = []
    for field in pop_id:
        id_list.append(field["id"])
    movie_detail = []
    for id in id_list:
        detail_req = set_tmdb(
            'https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=', 2)
        data = eval(
            detail_req.text.replace('false', 'False').replace('null', 'None'))
        movie_detail.append(data)
    return movie_detail


# 連mongoDB
def connection():
    client = pymongo.MongoClient(
        "mongodb+srv://" + user + ":" + password +
        "@movies.9gsbi.mongodb.net/<dbname>?retryWrites=true&w=majority")
    return client


# 在mongodb collection 中insert data
def insert():
    client = connection()
    client["popular_movies"]["movie_details"].insert_many(popular())


# 儲存圖片到mongodb
def image():
    mongo_client = connection()
    mongo_collection = mongo_client['popular_movies']['movie_details']
    data = mongo_collection.find({}, {
        "id": 1,
        "backdrop_path": 1,
        "poster_path": 1
    })

    # fs_backdrop = GridFS(mongo_client.popular_movies_img, collection='backdrop')
    # fs_poster = GridFS(mongo_client.popular_movies_img, collection='poster')
    data_img = []
    for d in data:
        d["backdrop_path"] = 'http://image.tmdb.org/t/p/original' + d[
            "backdrop_path"]
        d["poster_path"] = 'http://image.tmdb.org/t/p/original' + d[
            "poster_path"]
        backdrop_img = requests.get(d["backdrop_path"], timeout=10).content
        poster_img = requests.get(d["poster_path"], timeout=10).content
        d["backdrop_img"] = binary.Binary(backdrop_img)
        d["poster_img"] = binary.Binary(poster_img)
        data_img.append(d)
    mongo_client["popular_movies"]["images"].insert_many(data_img)


# 儲存圖片到本地
def local_img():
    mongo_client = connection()
    mongo_collection = mongo_client['popular_movies']['movie_details']
    data = mongo_collection.find({}, {
        "id": 1,
        "backdrop_path": 1,
        "poster_path": 1
    })

    # fs_backdrop = GridFS(mongo_client.popular_movies_img, collection='backdrop')
    # fs_poster = GridFS(mongo_client.popular_movies_img, collection='poster')
    data_img = []
    for d in data:
        d["backdrop_path"] = 'http://image.tmdb.org/t/p/original' + d[
            "backdrop_path"]
        d["poster_path"] = 'http://image.tmdb.org/t/p/original' + d[
            "poster_path"]
        backdrop_img = requests.get(d["backdrop_path"], timeout=10).content
        poster_img = requests.get(d["poster_path"], timeout=10).content
        with open('./../api/images/backdrop_path_' + str(d['id']) + '.jpg',
                  'wb') as f:
            f.write(backdrop_img)
        with open('./../api/images/poster_path_' + str(d['id']) + '.jpg',
                  'wb') as f:
            f.write(poster_img)


local_img()
