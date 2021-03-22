import requests
import re


class YahooMovieList():

    def __init__(self, href):
        self.href = href
        self.mongo_d = {}

    # 取得所有電影網址
    def movie_hrefs(self):
        r = requests.get(self.href)
        html = r.text
        data = re.findall('<main>[\s\S]*?</main>', html)[0].replace(" ", "")
        data = re.findall('<li>[\s\S]*?</li>', data)
        href = []
        for i in range(len(data)):
            movies = re.findall('<ahref=\"[\s\S]*?\"', data[i])
            movie_href = movies[0].replace("<ahref=\"", "").replace("\"", "")
            # 去除分頁資訊（一次只要一頁）
            if "page" in movie_href:
                pass
            else:
                href.append(movie_href)
        return href
