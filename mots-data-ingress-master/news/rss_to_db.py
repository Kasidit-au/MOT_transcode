from urllib.request import Request,urlopen
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import requests
import time
from pythainlp.util import thai_strftime
from datetime import datetime
import re
from hashlib import blake2b
from xml.etree.ElementTree import parse
from common import print_log
from configs import Config
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from models import Assignment as Assg, MasterTag as AssgMasterTag, AssignmentTag as AssgTag, AssignmentToLog as AssgLog
import peewee
from peewee import *
import json

with open('./gate1.json', 'r', encoding='utf-8') as f:
    gate1 = json.load(f)
with open('./gate2.json', 'r', encoding='utf-8') as f:
    gate2 = json.load(f)

# url of RSS feed
urls = {'thairath':['https://www.thairath.co.th/rss/news'],
        'prachachat':['https://www.prachachat.net/feed'],
        'posttoday': ['https://www.posttoday.com/rss/src/breakingnews.xml',
                     'https://www.posttoday.com/rss/src/politics.xml',
                     'https://www.posttoday.com/rss/src/economy.xml'],
        'sanook':['http://rssfeeds.sanook.com/rss/feeds/sanook/news.index.xml',
                  'http://rssfeeds.sanook.com/rss/feeds/sanook/news.politic.xml',
                  'http://rssfeeds.sanook.com/rss/feeds/sanook/news.economic.xml'],
        'manager':['http://www.manager.co.th/RSS/Home/Breakingnews.xml'],
        'naewna':['https://www.naewna.com/rss.php']
        }

from news_func import *
func_call = {'thairath':thairath,
             'prachachat':prachachat,
             'posttoday':posttoday,
             'sanook':sanook,
             'manager':mgronline,
             'naewna':naewna
}

#extract all links
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
news_rss = []
err_cnt = 0
for src,news_links_ls in urls.items():
    for news_link in news_links_ls:
            content = requests.get(news_link, headers=headers).content
            try:
                tree = ET.fromstring(content)
                for item in tree.iterfind('channel/item'):
                    link = item.findtext('link')
                    try:
                        news = func_call[src](link)
                        text = news['text']
                        tags_add = gate(text,gate1,gate2)
                        news['tags_added'] = tags_add
                        news_rss.append(news)
                    except:
                        pass
            except:
                err_cnt += 1
print(f'links collected, errors:{err_cnt}')
                

db = MySQLDatabase('mots-dev', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'mots-mariadb.mariadb.database.azure.com', 'port': 3306, 'user': 'xphys@mots-mariadb', 'password': 'ItsInternet'})

now = datetime.now()

tags_dict = {}
query = AssgMasterTag.select(AssgMasterTag.tag_id,AssgMasterTag.tag_name)
for i in query:
    tags_dict[i.tag_name] = str(i.tag_id)

masterSources = {
    'nn': 6,
    'bb': 7,
    'dn': 8,
    'mc': 9,
    'tr': 10,
    'pr': 11,
    'mt': 12,
    'pt': 13,
    'sn': 14
}

def call(data:dict):
    cnt_new = 0
    cnt_err = 0
    for d in data:
        try:
            assg = Assg()
            assg.news_ref = d.get('id')
            assg.news_name = d.get('heading')
            assg.news_detail = d.get('text')
            assg.news_link = d.get('url')
            assg.news_datetime = d.get('ts')
            assg.news_sync_datetime = now
            assg.assign_to_permission = 1
            assg.asg_status = 10
            assg.is_active = 1
            assg.news_source = masterSources.get(assg.news_ref.split('-')[0])
            assg.save()
            if d.get('tags_added'):
                for tashtag in d.get('tags_added'):
                        tagId = int(tags_dict[tashtag])
                        assgTag = AssgTag()
                        assgTag.asg = assg.asg_id
                        assgTag.tag = tagId
                        assgTag.is_system = 1  # 1 = assign by system
                        assgTag.create_datetime = now
                        assgTag.is_active = 1
                        assgTag.save()

            assgLog = AssgLog()
            assgLog.asg_id = assg.asg_id
            assgLog.create_datetime = now
            assgLog.save()
            cnt_new += 1

        except peewee.IntegrityError as ex:
            cnt_err += 1
        except Exception as ex:
            print_log(str(ex), 'ERROR')
            cnt_err += 1

    print_log(f'OK, Added:{cnt_new}, Error: {cnt_err}')

call(news_rss)

