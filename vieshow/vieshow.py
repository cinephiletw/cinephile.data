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
        'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p=' + str(n))
    movie_hrefs = vieshowMovieList.movie_hrefs()
    for href in movie_hrefs:
        mongo_d = {}
        movieDetail = movie_detail.MovieDetail(href)
        movieDetail.get_html()
        mongo_d['id'] = movieDetail.id()
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
        mongo_d['movie_source'] = [{
            'vieshow': 'https://www.vscinemas.com.tw/vsweb/film/' + href
        }]
        print(mongo_d)
        break


def Vieshow():
    perpage(1)
