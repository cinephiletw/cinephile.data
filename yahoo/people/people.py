import requests
import re
import time
import datetime
import pytz
# from . import movie_detail


class People():

    def __init__(self, html):
        self.html = html
        self.people_list = None

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

    def get_people_detail(self):
        pattern = '<div class=\"movie_intro_list\">[\s\S]*?</div>'
        replace_str = [
            '\n', '<div class=\"movie_intro_list\">', '<a href=[\s\S]*?\">',
            '</span>', '<span>', '</div>', '</a>'
        ]
        people = re.findall(pattern, self.html)
        for i in range(len(people)):
            for j in replace_str:
                people[i] = re.sub(j, '', people[i])
        self.people_list = people

    # 導演
    def director(self):
        director_list = self.people_list[0].split('、')
        for i in range(len(director_list)):
            director_list[i] = self.lan_identify(director_list[i])
        return director_list

    # 演員
    def cast(self):
        cast_list = self.people_list[1].split('、')
        for i in range(len(cast_list)):
            cast_list[i] = self.lan_identify(cast_list[i])
        return cast_list
