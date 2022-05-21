from urllib.request import Request,urlopen
from xml.etree.ElementTree import parse
from bs4 import BeautifulSoup
import json
import requests
import time
from pythainlp.util import thai_strftime
from datetime import datetime
import re
from hashlib import blake2b
from xml.etree.ElementTree import parse

with open('./mastertags-keywords.json','r',encoding='utf-8') as file:
    kw_ls = json.load(file)
    kw_list = kw_ls['Keyword']

# url of RSS feed
urls = {'thairath':['https://www.thairath.co.th/rss/news'],
        'prachachat':['https://www.prachachat.net/feed'],
        'mthai':['http://news.mthai.com/feed',
                'http://news.mthai.com/category/politics-news/feed',
                'http://news.mthai.com/category/world-news/feed',
                'http://news.mthai.com/category/general-news/feed'],
        'posttoday': ['https://www.posttoday.com/rss/src/breakingnews.xml',
                     'https://www.posttoday.com/rss/src/politics.xml',
                     'https://www.posttoday.com/rss/src/economy.xml'],
        'sanook':['http://rssfeeds.sanook.com/rss/feeds/sanook/news.index.xml',
                  'http://rssfeeds.sanook.com/rss/feeds/sanook/news.politic.xml',
                  'http://rssfeeds.sanook.com/rss/feeds/sanook/news.economic.xml']
        }

from news_func import *
func_call = {'thairath':thairath,
             'prachachat':prachachat,
             'mthai':mthai,
             'posttoday':posttoday,
             'sanook':sanook
}

#extract all links
news_rss = []
for src,news_links_ls in urls.items():
    for news_link in news_links_ls:
            req = Request(news_link, headers={'User-Agent': 'Mozilla/5.0'})
            var_url = urlopen(req)
            xmldoc = parse(var_url)
            for item in xmldoc.iterfind('channel/item'):
                link = item.findtext('link')
                try:
                    news = func_call[src](link)
                    text = news['text']
                    tags_add = add_tag(text,kw_list)
                    news['tags_added'] = tags_add
                    news_rss.append(news)
                except:
                    pass


with open('./_shared/rss_feed_news.json','w',encoding='utf-8') as file:
    json.dump(news_rss,file,ensure_ascii=False)





