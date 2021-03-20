import requests
import re


class VieshowMovieList():

    def __init__(self, href):
        self.href = href

    # 取得所有電影網址
    def movie_hrefs(self):
        r = requests.get(self.href)
        html = r.text
        data = re.findall(
            '<ul class=\"movieList\">[\s\S]*?<section class=\"pagebar\">',
            html)[0].replace(" ", "")
        data = re.findall('<sectionclass=\"infoArea\">[\s\S]*?</li>', data)
        href = []
        for d in data:
            href.append(
                d.split('<sectionclass=\"infoArea\">\r\n<h2><ahref=\"')
                [1].split('\">')[0])
        return href
