from .vieshow_movie_list import vieshow_movie_list
# methods:
#     movie_hrefs()

from .movie_detail import movie_detail
# methods:
#     get_html()
#     id()
#     title()
#     origin_title()
#     release_date()
#     director()
#     cast()
#     genre()
#     runtime()
#     poster()
#     content()
#     img()


def perpage(n):
    vieshowMovieList = vieshow_movie_list.VieshowMovieList(
        'https://www.vscinemas.com.tw/vsweb/film/coming.aspx?p=' + str(n))
    movie_hrefs = vieshowMovieList.movie_hrefs()
    movie_data = []
    for href in movie_hrefs:
        mongo_d = {}
        movieDetail = movie_detail.MovieDetail(href)
        movieDetail.get_html()
        mongo_d['title'] = movieDetail.title()
        mongo_d['origin_title'] = movieDetail.origin_title()
        mongo_d['release_date'] = movieDetail.release_date()
        mongo_d['director'] = movieDetail.director()
        mongo_d['cast'] = movieDetail.cast()
        mongo_d['genre'] = movieDetail.genre()
        mongo_d['runtime'] = movieDetail.runtime()
        mongo_d['poster_path'] = movieDetail.poster()
        mongo_d['content'] = movieDetail.content()
        mongo_d['image_path'] = movieDetail.img()
        mongo_d['source'] = [{
            'web_id': movieDetail.id(),
            'web_name': 'vieshow',
            'web_url': 'https://www.vscinemas.com.tw/vsweb/film/' + href
        }]
        movie_data.append(mongo_d)
    return movie_data


def Vieshow():
    index = 1
    movies = []
    while (True):
        try:
            movies.extend(perpage(index))
            index += 1
        except:
            break
    return movies
