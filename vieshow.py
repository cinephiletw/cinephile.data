from vieshow import vieshow_movie_list
# methods:
#     movie_herfs()


def perpage(n):
    vieshowMovieList = vieshow_movie_list.VieshowMovieList(
        'https://www.vscinemas.com.tw/vsweb/film/index.aspx?p=' + str(n))
