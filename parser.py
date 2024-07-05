import requests
import json
import time

import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='test_for_ictis')

cursor = cnx.cursor()


url = 'https://webictis.sfedu.ru/schedule-api/?query=%D0%93-412'

for i in range(20):
    time.sleep(3)
    if i < 10:
        rez = requests.get(f'https://webictis.sfedu.ru/schedule-api/?query=%D0%93-40{i}')
    else:
        rez = requests.get(f'https://webictis.sfedu.ru/schedule-api/?query=%D0%93-4{i}')

    print(rez.text)
    parse_mass = json.loads(rez.text)
    try:
        aud_rez = requests.get(f'https://webictis.sfedu.ru/schedule-api/?group={parse_mass["table"]["group"]}&week=15')
        rez_mass = json.loads(aud_rez.text)
        for ind in range(7):
            for timer, day in zip(rez_mass["table"]["table"][1], rez_mass["table"]["table"][2+ind]):
                if timer.lower() != 'время':
                    cursor.execute(f'''INSERT INTO `schedule`(`time_start`, `time_end`, `date`, `auditory`, `event`) VALUES ('{timer.split("-")[0]}:00','{timer.split("-")[1]}:00','{date}','{rez_mass["table"]["name"]}','{day}')''')
                else:
                    date = day[day.find(',')+1:]
                    if 'мая' in date:
                        date = "2024-" + "05-" + date[:day.find(" ")-3]
                    elif 'июня' in date:
                        date = "2024-" + "06-" + date[:day.find(" ")]
                    print(date)
    except:
        aud_rez = 'anlucky'
        print(aud_rez)
    cnx.commit()


cnx.close()