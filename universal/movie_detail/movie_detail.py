import requests
import re
import time
import datetime
import pytz


class MovieDetail():

    def __init__(self, href):
        self.href = 'https://www.u-movie.com.tw/cinema/' + href
        self.total_html = ''
        self.title_area_html = ''
        self.info_area_html = ''
        self.movie_info_list = []

    # 取得html
    def get_html(self):
        self.total_html = requests.get(self.href).text
        title_area_pattern = '<div class=\"col-12 col-xl-6 col-md-8 text-center padding-60px-tb\">[\s\S]*?</div>'
        self.title_area_html = re.findall(title_area_pattern,
                                          self.total_html)[0]
        info_area_pattern = '<div class=\"col-12 col-lg-6 padding-four-half-all lg-padding-eight-lr md-padding-30px-lr padding-five-tb md-padding-nine-half-tb sm-padding-15px-lr sm-padding-50px-tb wow fadeInRight bg-very-light-gray\"[\s\S]*?</section>'
        self.info_area_html = re.findall(
            info_area_pattern, self.total_html)[0].replace(' ', '').replace(
                '\n', '').replace('\t', '').replace('\r', '')
        movie_info_list_pattern = '<divclass=\"feature-content\">[\s\S]*?</div>'
        self.movie_info_list = re.findall(movie_info_list_pattern,
                                          self.info_area_html)

    # 中文標題
    def title(self):
        try:
            return self.title_area_html.split(
                '<p class=\"text-large text-uppercase letter-spacing-2 alt-font text-light-gray d-inline-block\" style=\"text-shadow: black 0.1em 0.1em 0.2em\">'
            )[1].split('</p>')[0]
        except:
            return None

    # 英文標題
    def origin_title(self):
        try:
            return self.title_area_html.split(
                '<h3 class=\"alt-font text-white-2 font-weight-600\" style=\"text-shadow: black 0.1em 0.1em 0.2em\">'
            )[1].split('</h3>')[0]
        except:
            return None

    # 片長
    def runtime(self):
        try:
            runtime_str = self.movie_info_list[2].split(
                '片長</mark><pclass="width-95sm-width-100">')[1].split(
                    '</p>')[0].replace('分', '')
            if '小時' in runtime_str:
                runtime_int = int(runtime_str.split('小時')[0]) * 60 + int(
                    runtime_str.split('小時')[1])
            else:
                runtim_int = int(runtime_str)
            return runtime_int
        except:
            return None

    # 簡介
    def content(self):
        try:
            content_str = self.movie_info_list[3]
            content_str = content_str.split(
                '<divclass=\"feature-content\"><markclass=\"text-largebg-very-light-grayborder-bottom\">劇情簡介</mark><pclass=\"width-95sm-width-100\">'
            )[1].split(
                '<ahref=\"javascript:history.back();\"class=\"btnbtn-smallbtn-roundedbtn-dark-gray\">回上一頁</a>'
            )[0]
            return content_str
        except:
            return None

    # 以下是人名相關爬蟲
    def lan_identify(self, text):
        # 判斷是否含中英文
        en = re.compile(r'[A-Za-z]')
        tw = re.compile(u'[\u4e00-\u9fa5]+')
        has_en = bool(en.search(text))
        has_tw = bool(tw.search(text))
        # 中英都有
        if has_tw == True and has_en == True:
            text = {
                "name_tw": text.split('(')[0].replace(' ', ''),
                "name_en": text.split('(')[1].split(')')[0]
            }
        # 只有中文
        elif has_tw == True and has_en == False:
            text = {"name_tw": text.replace(' ', '')}
        # 只有英文
        elif has_tw == False and has_en == True:
            text = {"name_en": text.replace(' ', '')}
        else:
            text = None
        return text

    # 導演
    def director(self):
        try:
            director_str = self.movie_info_list[0]
            director_str = director_str.split(
                '導演</mark><pclass=\"width-95sm-width-150\">')[1].split(
                    '</p>')[0]
            director_list = director_str.split('、')
            for i in range(len(director_list)):
                director_list[i] = self.lan_identify(director_list[i])
            return director_list
        except:
            return None

    # 演員
    def cast(self):
        try:
            cast_str = self.movie_info_list[1]
            cast_str = cast_str.split(
                '卡司</mark><pclass=\"width-95sm-width-100\">')[1].split(
                    '</p>')[0]
            cast_list = cast_str.split('、')
            for i in range(len(cast_list)):
                cast_list[i] = self.lan_identify(cast_list[i])
            return cast_list
        except:
            return None
