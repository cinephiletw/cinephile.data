
import requests
import csv
import pandas
from bs4 import BeautifulSoup

web = requests.get('https://movies.yahoo.com.tw/movie_thisweek.html')
content = BeautifulSoup(web.text, 'html.parser')
#獲取電影標題
info_item = content.find_all('div','release_info')
for item in info_item:
    name = item.find('div','release_movie_name').a.text.strip() #a為標籤.text為取得字串 strip()是刪除頭尾空格
    e_name = item.find('div','en').a.text.strip()
    level = item.find('div','leveltext').span.text      #期待度
    release_time = item.find('div','release_movie_time').text.split(':')[-1].strip()
    #split 將日期透過冒號（：）來分割，再使用 -1 取出最後一個位置，也就會是日期
    print('{}({}) 期待度:{}{}'.format(name, e_name, level, release_time))

#匯出到CSV


with open('moviesOutput.csv','w',newline='')as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["電影片名","英文電影片名","觀眾期待度","上映日期"])
    for item in info_item:
        name = item.find('div','release_movie_name').a.text.strip() 
        e_name = item.find('div','en').a.text.strip()
        level = item.find('div','leveltext').span.text    
        release_time = item.find('div','release_movie_time').text.split(':')[-1].strip()
        writer.writerow([name, e_name, level, release_time])