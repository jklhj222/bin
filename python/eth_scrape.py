#!/usr/bin/env python3
# https://morvanzhou.github.io/tutorials/data-manipulation/scraping/2-01-beautifulsoup-basic/
""" Created on Sun Aug 12 13:58:48 2018@author: jklhj """

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


headers = {'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

req = Request(url='https://www.coingecko.com/zh-tw/%E5%8C%AF%E7%8E%87%E5%9C%96/%E4%BB%A5%E5%A4%AA%E5%B9%A3/twd',
              headers=headers)

# if has Chinese, apply decode()
html = urlopen(req).read().decode('utf-8')

soup = BeautifulSoup(html, features='lxml')

print(soup.p.b)
#print(str(soup.p.b).split('>')[1].split('<')[0])


#file = open('test2.txt', 'w')

#file.write(html)

#print(html)
