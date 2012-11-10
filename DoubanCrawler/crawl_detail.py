#!/usr/bin/env python
# -*- coding:utf-8 -*-

# crawl_detail.py
# Crawl detail of the top250 movie on douban

import urllib2
import string
import bs4
import time
import os


if not os.path.exists('doc'):
    os.mkdir('doc')

if not os.path.exists('doc/detail'):
    os.mkdir('doc/detail')

origin_url = r'http://movie.douban.com/top250?format=text'

while True:
    try:
        html = urllib2.urlopen(origin_url)
        break
    except:
        time.sleep(3)
        continue

soup = bs4.BeautifulSoup(html)
movies = soup.select('.item')
movie_urls = []

for movie in movies:
    movie_urls.append(movie.select('a')[0]['href'])

rating_pos = 1
for url in movie_urls:
    time.sleep(3)
    print "Crawl movie %d" % rating_pos
    while True:
        try:
            html = urllib2.urlopen(url)
            break
        except:
            time.sleep(3)
            continue

    soup = bs4.BeautifulSoup(html)

    name = soup.select('h1 > span')[0].text.strip()

    detail_file = open("doc/detail/" + name + '.txt', 'w')

    year = soup.select('h1 > span')[1].text.strip('()')

    infos = soup.select('#info')[0]

    director = infos.select('a[rel="v:directedBy"]')[0].text.strip()
    playwriters = infos.select('span')[2].text.split(':')[-1].strip()
    actors = '/'.join([star.text.strip()
                       for star in infos.select('a[rel="v:starring"]')])
    movie_type = '/'.join([genre.text.strip()
                     for genre in infos.select('span[property="v:genre"]')])

    info_text = infos.text.strip().split('\n')
    nickname = info_text[-2].split(':')[-1].strip()
    length = info_text[-3].split(':')[-1].strip()
    onscreen = info_text[-4].split(':')[-1].strip()
    lang = info_text[-5].split(':')[-1].strip()
    area = info_text[-6].split(':')[-1].strip()

    #(director, playwriters, actors,
    # movie_type, area, lang, onscreen, length,
    # nickname, drop) = [t.split(':')[-1].strip() for t in info_text]

    imdb_link = infos.select('a[rel="nofollow"]')[-1]['href']

    movie_info_list = ["%i" % rating_pos, name, year, director,
                       playwriters, actors, movie_type, area, lang,
                       onscreen, length, nickname, imdb_link]
    wrt_string = '|'.join(movie_info_list) + '\n\n'
    detail_file.write(wrt_string.encode("utf-8"))

    print "Finish crawl basic info"

    rating_score = soup.select('[property="v:average"]')[0].text
    votes = soup.select('[property="v:votes"]')[0].text
    stars_text = soup.select('.rating_wrap')[0].text.strip().split()
    one_star = stars_text[-1].strip()
    two_star = stars_text[-2].strip()
    three_star = stars_text[-3].strip()
    four_star = stars_text[-4].strip()
    five_star = stars_text[-5].strip()
    rating_info_list = [rating_score, votes, five_star,
                        four_star, three_star, two_star, one_star]
    wrt_string = '|'.join(rating_info_list) + '\n\n'
    detail_file.write(wrt_string.encode("utf-8"))

    print "Finish crawl rating info"

    tags = soup.select('#db-tags-section')[0].select('a')
    wrt_string = '|'.join([tag.text.strip() for tag in tags]) + '\n\n'
    detail_file.write(wrt_string.encode('utf-8'))

    print "Finish crawl tags"

    summary = soup.select('[property="v:summary"]')[0].text
    wrt_string = summary + '\n\n'
    detail_file.write(wrt_string.encode('utf-8'))

    comments_num = string.atoi(soup.select('a[href="comments"]')[0]
                               .text.split()[1].strip())

    # crawl award
    time.sleep(3)
    print "Crawling award page"
    award_url = url + 'awards/'
    while True:
        try:
            html = urllib2.urlopen(award_url).read()
            break
        except:
            time.sleep(3)
            continue
    soup = bs4.BeautifulSoup(html)

    award_classes = soup.select('div[class="awards"]')
    awards = {}
    for award_class in award_classes:
        head = award_class.select('h2')[0].text.strip()
        head_awards = [' '.join(a.text.split())
                       for a in award_class.select('ul[class="award"]')]
        awards[head] = head_awards

    for p in awards:
        wrt_string = p + ':' + '|'.join(awards[p]) + '\n'
        detail_file.write(wrt_string.encode('utf-8'))

    detail_file.write('\n')

    print "Finish crawl award page"

    # crawl brief comments
    time.sleep(3)
    print "Crawling comment pages"
    comment_base_url = url + "comments?sort=vote&start="
    comments_page = (comments_num + 19) / 20

    wrt_string = "%i" % comments_num + '\n'
    detail_file.write(wrt_string.encode('utf-8'))

    crawl_count = 0
    for i in range(comments_page):
        if i % 50 == 0:
            time.sleep(3)
        print "Start crawlint comment page %d" % i
        comment_url = comment_base_url + ("%i" % (i * 20))
        while True:
            try:
                html = urllib2.urlopen(comment_url).read()
                time.sleep(1)
                crawl_count += 1
                break
            except:
                time.sleep(3)
                continue

        if crawl_count >= 150:
            time.sleep(20 * 60)
            break;

        soup = bs4.BeautifulSoup(html)
        comments = soup.select('.comment')
        for comment in comments:
            commenter = comment.select('a')[-1].text.strip()
            useful = comment.select('.votes')[0].text.strip()
            content = comment.select('.w490')[0].text.strip()
            comment_time = comment.select('.ml8')[0].text.strip()
            star = "0"
            if comment.select('.allstar50'):
                star = "5"
            elif comment.select('.allstar40'):
                star = "4"
            elif comment.select('.allstar30'):
                star = "3"
            elif comment.select('.allstar20'):
                star = "2"
            elif comment.select('.allstar10'):
                star = "1"

            comment_info_list = [commenter,
                                 comment_time, star, content, useful]
            wrt_string = '|'.join(comment_info_list) + '\n'
            detail_file.write(wrt_string.encode('utf-8'))

        print "Finish crawling comment page %d" % i

    print "Finish crawling movie %d" % rating_pos

    rating_pos = rating_pos + 1
