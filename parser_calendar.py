
import segno
import requests
import json
import time
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import unquote
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

sec_calend = souper.find('section', _class='announcements-container')
mass = souper.findAll('div', {"class" :'an-container'})

for i in mass:
    data =i.find('span', {"class": 'an-date'}).text.split('.')
    date = data[2]+'-'+data[1]+'-'+data[0]

    qrcode = segno.make_qr(i.find('a', {"class" :'an-title'})['href'])
    qrcode.save(f"{unquote(i.find('a', {'class' :'an-title'})['href']).split('/')[-2]}"+'.png')
    cursor.execute(f'''INSERT INTO `events`(`date`, `title`, `uri`, `qr`) VALUES ('{date}','{i.find('a', {"class" :'an-title'}).text}','{i.find('a', {"class" :'an-title'})['href']}','{i.find('a', {"class" :'an-title'})['href'].split('/')[-2]+'.png'}')''')

cnx.commit()
cnx.close()


