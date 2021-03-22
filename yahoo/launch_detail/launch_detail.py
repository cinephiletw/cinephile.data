import requests
import re
import time
import datetime
import pytz
# from . import movie_detail


class LaunchDetail():

    def __init__(self, html):
        self.html = html
        self.detail_list = None

    def get_detail_list(self):
        pattern = '<span>[\s\S]*?</span>'
        replace_str = ['[\s\S]*?：', '</span>']
        detail = re.findall(pattern, self.html)[:4]
        for i in range(4):
            for j in replace_str:
                detail[i] = re.sub(j, "", detail[i])
        self.detail_list = detail

    # 上映日期，以utc timestamp 儲存
    def release_date(self):
        try:
            tw = pytz.timezone('Asia/Taipei')
            release = self.detail_list[0]
            dt = datetime.datetime.strptime(release,
                                            '%Y-%m-%d').replace(tzinfo=tw)
            dt = dt.astimezone(pytz.utc)
            return time.mktime(dt.timetuple())
        except:
            return None

    # 片長，以分鐘儲存
    def runtime(self):
        try:
            runtime = 0
            if len(self.detail_list[1]) > 3:
                runtime = (int(self.detail_list[1][0]) * 10 +
                           int(self.detail_list[1][1])) * 60
                runtime += (int(self.detail_list[1][3]) * 10 +
                            int(self.detail_list[1][4]))
            else:
                runtime += (int(self.detail_list[1][3]) * 10 +
                            int(self.detail_list[1][4]))
            return runtime
        except:
            return None

    # 發行公司
    def company(self):
        try:
            return self.detail_list[2]
        except:
            return None

    # imdb 分數
    def imdb_rate(self):
        try:
            return float(self.detail_list[3])
        except:
            return None
