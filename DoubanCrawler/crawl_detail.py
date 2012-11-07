#!/usr/bin/env python
# -*- coding:utf-8 -*-

# crawl_detail.py
# Crawl detail of the top250 movie on douban

import urllib2
import string
import bs4

origin_url = r'http://movie.douban.com/top250?format=text'

def show(*args):
    for a in args:
        print a

while True:
    try:
        html = urllib2.urlopen(origin_url)
        break;
    except:
        continue;

soup = bs4.BeautifulSoup(html)
movies = soup.select('.item')
movie_urls = []

for movie in movies:
    movie_urls.append(movie.select('a')[0]['href'])


print len(movie_urls)
for url in movie_urls:
    print url
    while True:
        try:
            html = urllib2.urlopen(url)
            break;
        except:
            continue;

    soup = bs4.BeautifulSoup(html)
    
    name = soup.select('h1 > span')[0].text.strip()
    year = soup.select('h1 > span')[1].text.strip('()')
    
    infos = soup.select('#info')[0]
    '''
    director = infos.select('a[ref="v:directedBy"]')[0].text.strip()
    playwriters = '/'.join([ writer.text.strip() 
        for writer in infos.select('span')[2].select('a') ])
    actors = '/'.join([ actor.text.strip 
        for actor in infos.select('a[rel="v:starring"]') ])
    movie_type = '/'.join([ t.text.strip() 
        for t in infos.select('span[property="v:genre"]') ])
   ''' 
    info_text = infos.text.strip().split('\n')
    '''
    area = info_text[4].split(':')[-1].strip()
    lang = info_text[5].split(':')[-1].strip()
    onscreen = info_text[6].split(':')[-1].strip()
    length = info_text[7].split(':')[-1].strip()
    nickname = info_text[8].split(':')[-1].strip()
'''
    (director, playwriters, actors, movie_type, 
            area, lang, onscreen, length, nickname, drop) = [ 
                    t.split(':')[-1].strip() for t in info_text ]

    imdb_link = infos.select('a[rel="nofollow"]')[0]['href']

    rating = soup.select('[property="v:average"]')[0].text
    votes = soup.select('[property="v:votes"]')[0].text
    stars_text = soup.select('.rating_wrap')[0].text.strip().split()
    one_star = stars_text[-1].strip()
    two_star = stars_text[-2].strip()
    three_star = stars_text[-3].strip()
    four_star = stars_text[-4].strip()
    five_star = stars_text[-5].strip()

    summary = soup.select('[property="v:summary"]')[0].text
    comments_num = string.atoi(
            soup.select('a[href="comments"]')[0].text.split()[1].strip())

    show(director,playwriters,actors,movie_type,area,lang,onscreen,length,
            nickname,imdb_link,rating,votes,stars_text,one_star,two_star, three_star,
            four_star,five_star,summary,comments_num)
    
    # crawl award
    award_url = url + 'awards/'
    html = urllib2.urlopen(award_url).read()
    soup = bs4.BeautifulSoup(html)

    award_classes = soup.select('div[class="awards"]')
    awards = {}
    for award_class in award_classes:
        head = award_class.select('h2')[0].text.strip()
        head_awards = [ ' '.join(a.text.split()) 
                for a in award_class.select('ul[class="award"]')]
        awards[head] = head_awards
        #print awards
    
   # show(award_url,awards)
   # break;

    # crawl brief comments
    comment_base_url = url + "comments?sort=vote&start="
    comments_page = (comments_num + 19) / 20

    for i in range(comments_page):
        comment_url = comment_base_url + ("%i" % (i * 20))
        html = urllib2.urlopen(comment_url).read()
        soup = bs4.BeautifulSoup(html)
        comments = soup.select('.comment')
        for comment in comments:
            commenter = comment.select('a')[-1].text.strip()
            useful = string.atoi(comment.select('.votes')[0].text.strip())
            content = comment.select('.w490')[0].text.strip()
            comment_time = comment.select('.ml8')[0].text.strip()
            star = 0
            if comment.select('allstar50'):
                star = 5
            elif comment.select('allstar40'):
                star = 4
            elif comment.select('allstar30'):
                star = 3
            elif comment.select('allstar20'):
                star = 2
            elif comment.select('allstar10'):
                star = 1
        show(commenter,useful,content,comment_time,star)
        break;
    break;

