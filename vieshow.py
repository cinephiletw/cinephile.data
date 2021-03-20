from vieshow import vieshow_movie_list
# methods:
#     movie_hrefs()

from vieshow import movie_detail
# methods:
#     get_html()
#     id()
#     title()
#     origin_title()
#     release_date()


def perpage(n):
    vieshowMovieList = vieshow_movie_list.VieshowMovieList(
        'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p=' + str(n))
    movie_hrefs = vieshowMovieList.movie_hrefs()
    for href in movie_hrefs:
        movieDetail = movie_detail.MovieDetail(href)
        movieDetail.get_html()
        print(movieDetail.genre())
        break


perpage(1)
