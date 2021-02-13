from yahoo import yahoo_movie_list
# methods:
#     movie_herfs()

from yahoo import movie_detail
# methods:
#     get_html()
#     id()
#     title()
#     origin_title()
#     content()
#     genre()
#     poster()
#     image()

from yahoo import launch_detail
# methods:
#     get_detail_list()
#     release_date()
#     runtime()
#     company()
#     imdb_rate()

from yahoo import people
# methods:
#     get_people_detail()
#     director()
#     cast()

from mongoDAO import mongodb_for_data


def main():
    n = 1
    while (n != 9):
        perpage(n)
        n += 1


def perpage(n):
    yahooMovieList = yahoo_movie_list.YahooMovieList(
        'https://movies.yahoo.com.tw/movie_intheaters.html?page=' + str(n))
    movie_herfs = yahooMovieList.movie_herfs()
    mongodb = mongodb_for_data.MongoDb()
    mongodb.connection()
    mongodb.find_max_movie_id()

    for herf in movie_herfs:
        mongo_d = {}

        movieDetail = movie_detail.MovieDetail(herf)
        movieDetail.get_html()
        mongo_d['id'] = movieDetail.id()
        mongo_d['title'] = movieDetail.title()
        mongo_d['origin_title'] = movieDetail.origin_title()
        mongo_d['content'] = movieDetail.content()
        mongo_d['genre'] = movieDetail.genre()
        mongo_d['poster_path'] = movieDetail.poster()
        mongo_d['image_path'] = movieDetail.image()

        launchDetail = launch_detail.LaunchDetail(movieDetail.sub_info_html)
        launchDetail.get_detail_list()
        mongo_d['release_date'] = launchDetail.release_date()
        mongo_d['runtime'] = launchDetail.runtime()
        mongo_d['company'] = launchDetail.company()
        mongo_d['imdb_rate'] = launchDetail.imdb_rate()

        peo = people.People(movieDetail.total_html)
        peo.get_people_detail()
        mongo_d['director'] = peo.director()
        mongo_d['cast'] = peo.cast()

        mongodb.insert(mongo_d)


if __name__ == '__main__':
    main()
