import requests
import re
import time
import datetime
import pytz


class UniversalMovieList():

    def __init__(self, href):
        self.href = href

    # 取得所有電影網址和上映日期
    def movie_hrefs(self):
        r = requests.get(self.href)
        html = r.text.replace(' ', '').replace('\r', '').replace('\n', '')
        data = re.findall(
            '<divclass=\"col-12col-lg-4col-md-6last-paragraph-no-marginmd-margin-50px-bottomsm-margin-30px-bottom\">[\s\S]*?</div></div></div>',
            html)
        movie_link = []
        for d in data:
            href_str = d.split('<ahref=\"')[1].split('\">')[0]
            release_str = d.split('上映日期:')[1].split('</p>')[0]
            tw = pytz.timezone('Asia/Taipei')
            dt = datetime.datetime.strptime(release_str,
                                            '%Y-%m-%d').replace(tzinfo=tw)
            dt = dt.astimezone(pytz.utc)
            movie_link.append([href_str, time.mktime(dt.timetuple())])
        return movie_link
