import requests
from datetime import datetime
import csv
import json
from bs4 import BeautifulSoup
import json
import datetime
import requests
from lxml import html
from urllib.request import urlopen
import time
from pythainlp.util import thai_strftime
from datetime import datetime
import re
from hashlib import blake2b


def iso_date(x: str):
    months = {
        'ม.ค.': '01', 'มกราคม': '01',
        'ก.พ.': '02', 'กุมภาพันธ์': '02',
        'มี.ค.': '03', 'มีนาคม': '03',
        'เม.ย.': '04', 'เมษายน': '04',
        'พ.ค.': '05', 'พฤษภาคม': '05',
        'มิ.ย.': '06', 'มิถุนายน': '06',
        'ก.ค.': '07', 'กรกฎาคม': '07',
        'ส.ค.': '08', 'สิงหาคม': '08',
        'ก.ย.': '09', 'กันยายน': '09',
        'ต.ค.': '10', 'ตุลาคม': '10',
        'พ.ย.': '11', 'พฤศจิกายน': '11',
        'ธ.ค.': '12', 'ธันวาคม': '12',
        'January': '01','Jan':'01',
        'February': '02','Feb':'02',
        'March': '03','Mar':'03',
        'April': '04','Apr':'04',
        'May': '05','May':'05',
        'June': '06','Jun':'06',
        'July': '07','Jul':'07',
        'August': '08','Aug':'08',
        'September': '09','Sep':'09','Sept':'09',
        'October': '10','Oct':'10',
        'November': '11','Nov':'11',
        'December': '12','Dec':12
    }
    dd = int(re.findall(r'\d{1,2}(?!\S)', x)[0])  # .zfill(2)
    for m in months.keys():
        if m in x:
            mm = int(months[m])
    try:
        yyyy = int(re.findall(r'\d{4}', x)[0]) - 543
    except:
        yyyy = datetime.now().year
    try:
        tt = re.findall(r'\d{2}[:,.]\d{2}', x)[0]
        tt = tt.replace('.', ":")
        hh, min = tt.split(':')[0], tt.split(':')[1]
        hh = int(hh)
        min = int(min)
        ttime = datetime(yyyy, mm, dd, hh, min).isoformat()

    except IndexError:
        hh, min = None, None
        ttime = datetime(yyyy, mm, dd).isoformat()
    return ttime



def hashing(x:str,source:str):
    h = blake2b(digest_size=8)
    h.update(bytes(x,'utf-8'))
    return source+'-'+h.hexdigest()

def clean_text(text:str):
    text = text.replace(u'\xa0',u' ')
    text = text.replace(u'\n',u' ')
    text = text.replace(u'\t', u' ')
    return text
def thairath(link:str):
    # query the website and return the html to the page
    source = 'tr'
    page = requests.get(link)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    find_heading = soup.find_all('h1')
    heading = find_heading[0].text
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    find_tags = soup.find('div',attrs={'class',"css-sq8bxp evs3ejl16"})
    tags = []
    for tag in find_tags:
        if tag.text != '':
            tags.append(tag.text)
    find_date = soup.find_all('span')
    date_pattern = re.compile(r'\d+ .+ \d+ \d+:\d+ .+')
    for i in find_date:
        if bool(date_pattern.search(i.text)) == True:
            date = date_pattern.search(i.text).group(0)

    #find_date = soup.find_all(attrs={'class':'css-1cxbv8p evs3ejl7'})
    #span = find_date[0].find_all(attrs={'class':'css-x2q8w e1ui9xgn2'})
    #date = span[0].text
    result = {}
    result['id'] = hashing(heading,source)
    result['ts'] = iso_date(date)
    result['source'] = 'thairath'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result


def matichon(link:str):
    source = 'mc'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('time')['datetime']
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'matichon'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def naewna(link:str):
    source = 'nn'
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('div',class_='newsdate').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading,source)
    result['ts'] = ts
    result['source'] = 'naewna'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link

    return result

def bkkbiz(link:str): # need to correct date
    source = 'bb'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span',class_='f_right current_date').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    find_tags = soup.find_all('a',class_='btn-tags')
    tags = []
    for tag in find_tags:
        if tag.text != '':
            tags.append(tag.text)
    result = {}
    result['id']  = hashing(heading,source)
    result['ts'] = ts
    result['source'] = 'bkkbiz'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result

def dailynews(link:str):
    source = 'dn'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span',class_='date').text
    ts = iso_date(ts)
    find_text = soup.find_all('div',class_='entry textbox content-all')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading,source)
    result['ts'] = ts
    result['source'] = 'dailynews'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def prachachat(link:str):
    source = 'pr'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span',class_='td-post-date td-post-date-no-dot').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading,source)
    result['ts'] = ts
    result['source'] = 'prachachat'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def mthai(link:str):
    source = 'mt'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    page = requests.get(link,headers=headers)
    content = page.content
    soup = BeautifulSoup(content,'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('time',class_='entry-date published updated')['datetime']
    # date_pattern = re.compile(r'\d+\*\d+:\d+ .+')
    # for i in find_date:
    #     if bool(date_pattern.search(i.text)) == True:
    #         date = date_pattern.search(i.text).group(0)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading,source)
    result['ts'] = ts
    result['source'] = 'mthai'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def ch3(link:str):
        source = 'ch3'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        page = requests.get(link, headers=headers)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        heading = soup.find('h1').text
        ts = None
        # date_pattern = re.compile(r'\d+\*\d+:\d+ .+')
        # for i in find_date:
        #     if bool(date_pattern.search(i.text)) == True:
        #         date = date_pattern.search(i.text).group(0)
        find_text = soup.find_all('p')
        text = ''
        for t in find_text[5:]:
            txt = t.text.strip()
            text += txt
        text = clean_text(text)
        result = {}
        result['id'] = hashing(heading, source)
        result['ts'] = ts
        result['source'] = 'ch3'
        result['heading'] = heading
        result['text'] = text
        result['url'] = link
        return result

def posttoday(link:str):
    source = 'pt'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h2').text
    ts = soup.find('div', class_='date_time').text
    ts = iso_date(ts)
    article_intro = soup.find('div',class_='article-intro').text.strip()
    find_text = soup.find_all('p')
    text = ''
    text += article_intro
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    tags = []
    find_tags = soup.find_all('div',class_='box-tag')[0]
    for i in find_tags.find_all('li')[1:]:
        tag = i.text
        tags.append(tag)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'posttoday'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result


def sanook(link:str):
    source = 'sn'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span', class_='jsx-1665670616 infoItem').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text[:-3]:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    find_tags = soup.find_all('div',class_='jsx-545328869')[1]
    tags = []
    for tag in find_tags.find_all('a'):
        tags.append(tag.text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'sanook'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result


def standard(link:str):
    source = 'std'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('div', class_='meta-date').text
    ts = ts.replace('\n','')
    ts = datetime.strptime(ts, '%d.%m.%Y').isoformat()
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    find_tags = soup.find('div',class_='tags')
    tags = []
    for tag in find_tags.find_all('a'):
        tags.append(tag.text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'standard'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result

def mgronline(link:str):
    source = 'mgr'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    time = soup.find('time').text
    ts = iso_date(time)
    find_text = soup.find_all('div',class_='detail m-c-font-article')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'mgronline'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def khaosod(link:str):
    source = 'ks'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1',class_='udsg__main-title').text
    time = soup.find('span',class_='udsg__meta').text
    ts = iso_date(time)
    find_text = soup.find_all('p')[:-10]
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'khaosod'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result


def komchadluek(link:str):
    source = 'kc'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    time = soup.find('div',class_='article-date-news').text
    ts = iso_date(time)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'komchadluek'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

komchadluek('https://www.komchadluek.net/news/hotclip/461225')

def siamrath(link:str):
    source = 'sr'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    mr5 = soup.find_all('span',class_='mr5')
    time = mr5[1].text
    ts = iso_date(time)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'siamrath'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def ryt9(link:str):
    source = 'ryt9'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    datetime = soup.find('p',class_='date-time')
    time = datetime.text
    pattern = r'[a-zA-Z]+\s[a-zA-Z]+\s\d+,\s\d+\s\d+:\d+'
    x = re.search(pattern,time).group()
    print(x)
    ts = iso_date(time)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'ryt9'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def pptv(link:str):
    source = 'pptv'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    datetime = soup.find('time')
    time = datetime.text
    ts = iso_date(time)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'pptv'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result

def thansettakij(link:str):
    source = 'thk'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    time = soup.find('div',class_='date').text
    ts = iso_date(time)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    text = clean_text(text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'thk'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result




def add_tag(text:str,kw_list:dict):
    tags = []
    for key, val in kw_list.items():
        for k in val:
            if (k in text) and (key not in tags):
                tags.append(key)
    return tags


def gate(text:str,gate1:dict,gate2:dict):
    tags = []
    for mstag, tier1 in gate1.items():
        for t1 in tier1:
            if t1 in text:  # pass first gate
                if len(gate2[t1]) == 0:
                    if (t1 not in tags) and (mstag not in tags):
                        tags.append(mstag)
                        break
                else: # gate2[t2] not empty so we need to check
                    for t2 in gate2[t1]:
                        if (t2 in text) and (mstag not in tags):
                            tags.append(mstag)
                            break
    return tags

def parse_news(url:str):
    sites_ls = ['thairath', 'dailynews', 'matichon', 'bangkokbiz', 'naewna']
    site = None
    for s in sites_ls:
        if re.search(s,url):
            site = s
            break
    if site == 'thairath':
        try:
            return thairath(url)
        except:
            return 'N/A'
    elif site == 'matichon':
        try:
            return matichon(url)
        except:
            return 'N/A'
    elif site == 'naewna':
        try:
            return naewna(url)
        except:
            return 'N/A'
    elif site == 'bangkokbiz':
        try:
            return bkkbiz(url)
        except:
            return 'N/A'
    elif site == 'dailynews':
        try:
            return dailynews(url)
        except:
            return 'N/A'

