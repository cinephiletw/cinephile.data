import requests
import re


class MovieDetail():

    def __init__(self, href):
        self.href = href
        self.total_html = ""
        self.info_html = ""
        self.sub_info_html = ""

    # 取得html
    def get_html(self):
        self.total_html = requests.get(self.href).text

        info_pattern = '<div class=\"movie_intro_info_r\">[\s\S]*?<dl class=\"evaluatebox\">'
        self.info_html = re.findall(info_pattern, self.total_html)[0]
        sub_info_pattern = '<div class=\"level_name_box\">[\s\S]*?<div class=\"movie_intro_list\">'
        self.sub_info_html = re.findall(sub_info_pattern, self.info_html)[0]

    # 電影ID (yahoo)
    def id(self):
        try:
            return int(self.href.split("-")[-1])
        except:
            return None

    # 電影標題
    def title(self):
        pattern = '<h1>[\s\S]*?</h1>'
        replace_str = ['<h1>', '</h1>']

        try:
            title_data = re.findall(pattern, self.info_html)[0]
            for i in range(len(replace_str)):
                title_data = re.sub(replace_str[i], "", title_data)
            return title_data

        except:
            return None

    # 原文標題
    def origin_title(self):
        pattern = '<h3>[\s\S]*?</h3>'
        replace_str = ['<h3>', '</h3>']

        try:
            origin_title_data = re.findall(pattern, self.info_html)[0]
            for i in range(len(replace_str)):
                origin_title_data = re.sub(replace_str[i], "",
                                           origin_title_data)
            return origin_title_data
        except:
            return None

    # 簡介
    def content(self):
        pattern = '<div class=\"gray_infobox_inner\">[\s\S]*?<div class=\"btn_gray_info gabtn\"'
        try:
            content_data = re.findall(pattern, self.total_html)[0]
            content_data = content_data.split(
                '<span id=\'story\'>')[1].split('</span>')[0].strip().replace(
                    '</p>', '').replace('&nbsp;', '').replace('&hellip;', '')
            return content_data
        except:
            return None

    # 分類
    def genre(self):
        pattern = '<div class=\"level_name\">[\s\S]*?</a>'
        replace_str = [
            ' ', '\n', '<divclass=\"level_name\"><a[\s\S]*?\">', '</a>'
        ]

        genre_data = re.findall(pattern, self.sub_info_html)
        genre_list = []
        for i in range(len(genre_data)):
            for j in replace_str:
                genre_data[i] = re.sub(j, '', genre_data[i])
            # 如果含有"/" 拆出來
            if "/" in genre_data[i]:
                sub_genre_data = genre_data[i].split("/")
                for ele in sub_genre_data:
                    genre_list.append(ele)
            else:
                genre_list.append(genre_data[i])
        return genre_list

    # poster
    def poster(self):
        pattern = '<div class=\"movie_intro_foto\">[\s\S]*?<div class=\"color_btnbox\">'
        replace_str = [
            '<div class=\"movie_intro_foto\"><img src=\"',
            '\" alt[\s\S]*?<div class=\"color_btnbox\">'
        ]

        try:
            poster_data = re.findall(pattern, self.total_html)[0]
            for i in range(len(replace_str)):
                poster_data = re.sub(replace_str[i], "", poster_data)
            return poster_data
        except:
            return None

    # image
    def image(self):
        try:
            image_html = requests.get(
                'https://movies.yahoo.com.tw/movieinfo_photos.html/id=' +
                str(self.id())).text
            pattern = '<div class=\"pic\">[\s\S]*?<div class=\"movie_foto_num\">'
            image_data = re.findall(pattern, image_html)[0]
            image_data = image_data.split("<img src=\"")[1:]
            image_list = []
            for path in image_data:
                image_list.append(path.split("\"")[0])
            return image_list
        except:
            return None
