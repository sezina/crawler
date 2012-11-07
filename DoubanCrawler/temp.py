import urllib2
from bs4 import BeautifulSoup

url = "http://movie.douban.com/top250?format=text"

html = urllib2.urlopen(url).read()

soup = BeautifulSoup(html)

print soup.title
