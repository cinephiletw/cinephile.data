import requests
import re
import time
import datetime
import pytz


class MovieDetail():

    def __init__(self, href):
        self.href = 'https://www.vscinemas.com.tw/vsweb/film/' + href
        self.total_html = ""
        self.info_html = ""
        self.title_area_html = ""
        self.info_area_html = ""
        self.info_area_list = []
        self.content_html = ""
        self.img_html = ""

    # 取得html
    def get_html(self):
        self.total_html = requests.get(self.href).text
        info_pattern = '<div class=\"movieMain\"[\s\S]*?<div class=\"movieVersion\"'
        self.info_html = re.findall(info_pattern, self.total_html)[0]
        title_area_pattern = '<div class=\"titleArea\">[\s\S]*?</div>'
        self.title_area_html = re.findall(title_area_pattern, self.info_html)[0]

        info_area_pattern = '<div class=\"infoArea\">[\s\S]*?</div>'
        self.info_area_html = re.findall(info_area_pattern, self.info_html)[0]

        info_area_list_pattern = '<tr>[\s\S]*?</tr>'
        self.info_area_list = re.findall(info_area_list_pattern,
                                         self.info_area_html)
        content_pattern = '<div class=\"bbsArticle\">[\s\S]*?</div>'
        self.content_html = re.findall(content_pattern, self.total_html)[0]
        img_pattern = '<div id=\"photoBox\" class=\"moviePicture\"[\s\S]*?<footer'
        self.img_html = re.findall(img_pattern, self.total_html)[0]

    # 電影ID viewshow
    def id(self):
        try:
            return int(self.href.split("id=")[1])
        except:
            return None

    # 中文標題
    def title(self):
        try:
            return self.title_area_html.split('<h1>')[1].split('</h1>')[0]
        except:
            return None

    # 英文標題
    def origin_title(self):
        try:
            return self.title_area_html.split('<h2>')[1].split('</h2>')[0]
        except:
            return None

    # 上映日期，以utc timestamp 儲存
    def release_date(self):
        try:
            release = self.title_area_html.split('<time>上映日期：')[1].split(
                '</time>')[0]
            tw = pytz.timezone('Asia/Taipei')
            dt = datetime.datetime.strptime(release,
                                            '%Y/%m/%d').replace(tzinfo=tw)
            dt = dt.astimezone(pytz.utc)
            return time.mktime(dt.timetuple())
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
            director_str = self.info_area_list[0].split('<td><p>')[1].split(
                '</p></td>')[0].replace(' ', '')
            director_list = director_str.split('、')
            for i in range(len(director_list)):
                director_list[i] = self.lan_identify(director_list[i])
            return director_list
        except:
            return None

    # 演員
    def cast(self):
        try:
            cast_str = self.info_area_list[1].split('<td><p>')[1].split(
                '</p></td>')[0].replace(' ', '').replace('<br>', '').replace(
                    '\"', '').replace('(聲優)', '')
            cast_list = cast_str.split('、')
            for i in range(len(cast_list)):
                cast_list[i] = self.lan_identify(cast_list[i])
            return cast_list
        except:
            return None

    # 種類
    def genre(self):
        try:
            pattern = '<td>[\s\S]*?</td>'
            genre_str = re.findall(pattern, self.info_area_list[2])[1].replace(
                '<td>', '').replace('</td>', '').replace('/', '、')
            genre_list = genre_str.split('、')
            return genre_list
        except:
            return None

    # 片長
    def runtime(self):
        try:
            pattern = '<td>[\s\S]*?</td>'
            runtime_str = re.findall(pattern,
                                     self.info_area_list[3])[1].replace(
                                         '<td>',
                                         '').replace('</td>',
                                                     '').replace('/', '、')
            if '時' in runtime_str:
                hr_str = runtime_str.strip().split('時')[0]
                min_str = runtime_str.strip().split('時')[1].replace('分', '')
                return int(hr_str) * 60 + int(min_str)
            else:
                min_str = runtime_str.replace('分', '')
                return int(min_str)
        except:
            return None

    # 海報
    def poster(self):
        try:
            pattern = '<figure>[\s\S]*?</figure>'
            poster_html = re.findall(pattern, self.info_html)[0]
            poster_pre_path = poster_html.split('src=\"')[1].split('\"')[0]
            poster_path = 'https://www.vscinemas.com.tw/vsweb' + poster_pre_path.replace(
                '..', '')
            return poster_path
        except:
            return None

    # 內容
    def content(self):
        try:
            return self.content_html.replace(' ', '').replace(
                '<divclass="bbsArticle">',
                '').replace('<p>',
                            '').replace('</p>',
                                        '').replace('<br/>',
                                                    '').replace('</div>', '')
        except:
            return None

    # 劇照
    def img(self):
        try:
            pattern = '<img u=\"image\" src=\"..[\s\S]*?\" itemprop=\"thumbnail\">'
            img_path_str_list = re.findall(pattern, self.img_html)
            img_path_list = []
            for path in img_path_str_list:
                img_path_list.append(
                    'https://www.vscinemas.com.tw/vsweb' +
                    path.replace('<img u=\"image\" src=\"..', '').replace(
                        '\" itemprop=\"thumbnail\">', ''))
            return img_path_list
        except:
            return None
