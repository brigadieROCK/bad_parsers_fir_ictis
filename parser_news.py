import requests
import json
import time
from bs4 import BeautifulSoup
import mysql.connector

from selenium import webdriver
import warnings

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='test_for_ictis')

cursor = cnx.cursor()
warnings.filterwarnings('ignore')

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
new_client = webdriver.Chrome(options=options)

new_client.get('http://localhost/test_for_ictis/code.html')
time.sleep(3)


souper = BeautifulSoup(new_client.page_source, 'html.parser')


news = souper.find('div', {"class": 'container-news'}).find_all('div', {"class": 'new'})
for i in news:
    print('Название: ', i.find('a', {"class": 'title-new'}).text)
    print('Photo: ', i.find('img', {"class": 'attachment-post-thumbnail'})['src'])
    photo = requests.get(i.find('img', {"class": 'attachment-post-thumbnail'})['src'])
    open(f"photo-news/{i.find('img', {'class': 'attachment-post-thumbnail'})['src'].split('/')[-1]}", 'wb').write(photo.content)
    cursor.execute(f'''INSERT INTO `news`(`img`, `title`) VALUES ('{i.find('img', {'class': 'attachment-post-thumbnail'})['src'].split('/')[-1]}','{i.find('a', {"class": 'title-new'}).text}')''')


cnx.commit()
cnx.close()