#!/usr/bin/env python
# -*- coding:utf-8 -*-

# crawl_list.py
# Crawl the list of top250 movie on douban

import urllib2
from bs4 import BeautifulSoup



def show(*args):
    for arg in args:
        print arg

url = r'http://movie.douban.com/top250?format=text'
record_file = open('doc/top250.txt', 'w')

while True:
    try:
        html = urllib2.urlopen(url).read()
        break;
    except:
        continue;

soup = BeautifulSoup(html)
movies_infos = zip(soup.select('.item'), soup.select('.info'))

for (movie, info) in movies_infos:
    rating = movie.select('.m_order')[0].text.strip()
    detail_url = movie.select('a')[0]['href']
    name = movie.select('a')[0].text
    year = movie.select('.year')[0].text
    rating_score = movie.select('em')[0].text
    rating_num = movie.select('td[headers="m_rating_num"]')[0].text.strip()
    
    info_list = info.select('p')[0].text.strip().split('\n')
    director_actor = info_list[0].split(u'\xa0')
    director = director_actor[0].split(':')[-1].strip()
    actors = director_actor[-1].split(':')[-1].strip()

    area = info_list[-1].split('/')[-1].strip()
    brief_comment = ""
    if info.select('.inq'):
        brief_comment = info.select('.inq')[0].text.strip()

    record = '|'.join([rating, name, detail_url, rating_score, rating_num,
                       director, actors, year, area, brief_comment]) + '\n'
    record_file.write(record.encode('utf-8'))
    print record
  #  show(rating, detail_url, name, year, rating_score, rating_num,
   #         director, actors, area, brief_comment)

