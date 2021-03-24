from universal_movie_list import universal_movie_list
from movie_detail import movie_detail
# method
#     get_html()
#     title()
#     origin_title()
#     runtime()
#     content()
#     director()
#     cast()


def perpage(n):
    universalMovieList = universal_movie_list.UniversalMovieList(
        'https://www.u-movie.com.tw/cinema/page.php?data_nav=507&page_type=series&vid=5136'
    )
    movie_hrefs = universalMovieList.movie_hrefs()
    for href in movie_hrefs:
        mongo_d = {}
        movieDetail = movie_detail.MovieDetail(href[0])
        movieDetail.get_html()
        mongo_d['title'] = movieDetail.title()
        mongo_d['origin_title'] = movieDetail.origin_title()
        mongo_d['runtime'] = movieDetail.runtime()
        mongo_d['content'] = movieDetail.content()
        mongo_d['director'] = movieDetail.director()
        mongo_d['cast'] = movieDetail.cast()
        mongo_d['release_date'] = href[1]
        print(mongo_d)


perpage(1)
