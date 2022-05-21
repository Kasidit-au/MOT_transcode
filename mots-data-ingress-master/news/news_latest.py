# import sys, os
# cwd = os.getcwd()
# os.chdir(cwd)
# sys.path.append(cwd)
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
urls = {'dailynews':['https://dailynews.co.th'],
        'komchadluek':['https://www.komchadluek.net/'],
        'standard':['https://thestandard.co/homepage/'],
        'khaosod':['https://www.khaosod.co.th/home'],
        'matichon':['https://www.matichon.co.th/'],
        'bkkbiz':['https://www.bangkokbiznews.com/'],
        'siamrath':['https://siamrath.co.th/'],
        'ryt9':['https://www.ryt9.com/'],
        'pptv':['https://www.pptvhd36.com/'],
        'thansettakij':['https://www.thansettakij.com/'],
        }

from news_func import *
func_call = {'dailynews':dailynews,
             'komchadluek':komchadluek,
             'standard': standard,
             'khaosod': khaosod,
             'matichon': matichon,
             'bkkbiz' : bkkbiz,
             'siamrath':siamrath,
             'ryt9':ryt9,
             'pptv':pptv,
             'thansettakij':thansettakij,
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
news_latest = []
news_total = 0
err_cnt = 0
for src,news_links_ls in urls.items():
    for news_link in news_links_ls:
        content = requests.get(news_link, headers=headers).content
        soup = BeautifulSoup(content,'html.parser')
        links_anchor = soup.find_all('a',href=True)
        if src == 'dailynews' or src == 'komchadluek':
            for partial_url in links_anchor:
                matched = re.match("/.+/\d+", partial_url['href'])
                if bool(matched):
                    try:
                        link = news_link + partial_url['href']
                        news = func_call[src](link)
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'matichon':
            for link in links_anchor:
                matched = re.match('https://www.matichon.co.th/.+/news_\d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'bkkbiz':
            for link in links_anchor:
                matched = re.match('https://www.bangkokbiznews.com/news/detail/\d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'khaosod':
            for link in links_anchor:
                matched = re.match('https://www.khaosod.co.th/.+/news_\d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'siamrath':
            for link in links_anchor:
                matched = re.match('https://siamrath.co.th/n/d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'pptv':
            for link in links_anchor:
                matched = re.match('https://www.pptvhd36.com/news/.+/\d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        elif src == 'thansettakij':
            for link in links_anchor:
                matched = re.match('https://www.thansettakij.com/content/.+/\d+', link['href'])
                if bool(matched):
                    try:
                        news = func_call[src](link['href'])
                        text = news['text']
                        news['tags_added'] = gate(text,gate1,gate2)
                        news_latest.append(news)
                        news_total += 1
                    except:
                        pass
        # elif src == 'standard':
        #     for link in links_anchor:
        #         matched = re.match('https://thestandard.co/.+/', link['href'])
        #         if bool(matched):
        #             print(link['href'])



news_latest


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
    'sn': 14,
    'ks': 15
}

def call(data:dict):
    cnt_new = 0
    cnt_Int_err = 0
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
            cnt_Int_err += 1
        except Exception as ex:
            print_log(str(ex), 'ERROR')
            cnt_err += 1

    print_log(f'OK, Added:{cnt_new}, Integrity Error: {cnt_Int_err}, Errors: {cnt_err}')

call(news_latest)

