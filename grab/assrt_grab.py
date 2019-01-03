import requests
from bs4 import BeautifulSoup
import datetime
import re
import pymysql


def ass_grab():
    url = 'https://assrt.net/calendar#today'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
               'Upgrade-Insecure-Requests': '1'}
    res = requests.get(url, headers=headers)
    html = res.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    days = soup.find_all('td', {'class': 'day'})
    for day in days:
        date_time = day.get('id').replace('d', '12:00:00')
        # 影视播放时间
        date_time = datetime.datetime.strptime(date_time, '%H:%M:%S_%d_%m_%Y')
        stamp_time = int(date_time.timestamp())
        movies_list = day.find_all('p')
        for movies in movies_list:
            # 影视url
            movies_url = movies.find('a').get('href')
            # 英文名
            try:
                movies_english_name = movies.find('span').text
            except:
                movies_english_name = movies.find('a').text
            # 中文名，如果没有中文名则改为英文名
            movies_name = movies.find('a').get('title').replace(' 字幕', '')
            if movies_name == '' or 'Season' in movies_name:
                movies_name = movies_english_name
            # 季 与 集
            season_episode = re.search('S\d+ E\d+', str(movies)).group(0)

            # 数据库连接

