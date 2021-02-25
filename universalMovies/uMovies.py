import requests
import csv
import pandas
from bs4 import BeautifulSoup

web = requests.get('https://u-movie.com.tw/cinema/page.php?data_nav=507&page_type=series&vid=5136')
content = BeautifulSoup(web.text, 'html.parser')
#獲取電影標題
info_item = content.find_all('div','post-details')
for item in info_item:
    e_name = item.find('span','post-author text-extra-small text-medium-gray text-uppercase d-block margin-10px-bottom sm-margin-5px-bottom').a.text.strip()

    release_time = item.find('p','width-90 sm-width-100').text.split(':')[-1].strip()
    print(release_time)
  
   # print('{}({}) 期待度:{}{}'.format(name, e_name, level, release_time))

#匯出到CSV


with open('uMoviesOutput.csv','w',newline='')as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["英文電影片名","上映日期"])
    for item in info_item:
   
        e_name = item.find('span','post-author text-extra-small text-medium-gray text-uppercase d-block margin-10px-bottom sm-margin-5px-bottom').a.text.strip()
    
        release_time = item.find('p','width-90 sm-width-100').text.split(':')[-1].strip()
        writer.writerow([e_name, release_time])
