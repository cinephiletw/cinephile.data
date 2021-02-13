import requests
import re


class YahooMovieList():

    def __init__(self, herf):
        self.herf = herf
        self.mongo_d = {}

    # 取得所有電影網址
    def movie_herfs(self):
        r = requests.get(self.herf)
        html = r.text
        data = re.findall('<main>[\s\S]*?</main>', html)[0].replace(" ", "")
        data = re.findall('<li>[\s\S]*?</li>', data)
        herf = []
        for i in range(len(data)):
            movies = re.findall('<ahref=\"[\s\S]*?\"', data[i])
            movie_herf = movies[0].replace("<ahref=\"", "").replace("\"", "")
            # 去除分頁資訊（一次只要一頁）
            if "page" in movie_herf:
                pass
            else:
                herf.append(movie_herf)
        return herf
