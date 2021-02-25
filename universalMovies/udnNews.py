import requests
import csv
import pandas
from bs4 import BeautifulSoup

web = requests.get('https://udn.com/news/breaknews/1')
content = BeautifulSoup(web.text, 'html.parser')
s = content.select(".story-list__text h2")


with open('output.csv','w',newline='')as csv_file:
    writer=csv.writer(csv_file)
    writer.writerow(["標題"])
    for item in s[2:]:
        a=(item.text[1:-1])
        writer.writerow([a])