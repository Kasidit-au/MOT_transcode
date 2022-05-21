from bs4 import BeautifulSoup
import json
import datetime
import requests
from datetime import datetime
import re
from hashlib import blake2b

now = datetime.now()
ts = datetime.strftime(now, '%d/%m/%y %H:%M:%S')
keywords = ['M flow', 'ทางพิเศษ', 'มอร์เตอร์เวย์', 'พระราม 2', 'ประมูล', 'ใบขับขี่', 'ต่อใบขับขี่', 'รถไฟฟ้า', 'BTS',
            'สถานีกลาง', 'สถานีกลางบางซื่อ', 'รถไฟความเร็วสูง', 'รถไฟรางคู่', 'ล้มประมวล', 'ฮั๊วประมูล', 'เงินทอน']

urls = []
for key in keywords:
    url = f'https://www.googleapis.com/customsearch/v1?key=AIzaSyBh8-YNF5rR7Qw5ZvXEH6djcFXdRsCBbDo&cx=64d35653c32d248c2&dateRestrict=d1&q={key}'
    get = requests.get(url)
    content = get.content
    data = json.loads(content)
    if 'items' in data.keys():
        for i in data['items']:
            urls.append(i['link'])


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
    }
    dd = int(re.findall(r'\d{1,2}(?!\S)', x)[0])  # .zfill(2)
    for m in months.keys():
        if m in x:
            mm = int(months[m])
    yyyy = int(re.findall(r'\d{4}', x)[0]) - 543
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


def hashing(x: str, source: str):
    h = blake2b(digest_size=8)
    h.update(bytes(x, 'utf-8'))
    return source + '-' + h.hexdigest()


def thairath(link: str):
    # query the website and return the html to the page
    source = 'tr'
    page = requests.get(link)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    find_heading = soup.find_all('h1')
    heading = find_heading[0].text
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    find_tags = soup.find('div', attrs={'class', "css-sq8bxp evs3ejl16"})
    tags = []
    for tag in find_tags:
        if tag.text != '':
            tags.append(tag.text)
    find_date = soup.find_all('span')
    date_pattern = re.compile(r'\d+ .+ \d+ \d+:\d+ .+')
    for i in find_date:
        if bool(date_pattern.search(i.text)) == True:
            date = date_pattern.search(i.text).group(0)

    # find_date = soup.find_all(attrs={'class':'css-1cxbv8p evs3ejl7'})
    # span = find_date[0].find_all(attrs={'class':'css-x2q8w e1ui9xgn2'})
    # date = span[0].text
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = iso_date(date)
    result['source'] = 'thairath'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result


def matichon(link: str):
    source = 'mc'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('time')['datetime']
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'matichon'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result


def naewna(link: str):
    source = 'nn'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('div', class_='newsdate').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'naewna'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link

    return result


def bkkbiz(link: str):  # need to correct date
    source = 'bb'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span', class_='f_right current_date').text
    ts = iso_date(ts)
    find_text = soup.find_all('p')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    find_tags = soup.find_all('a', class_='btn-tags')
    tags = []
    for tag in find_tags:
        if tag.text != '':
            tags.append(tag.text)
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'bkkbiz'
    result['heading'] = heading
    result['text'] = text
    result['tags'] = tags
    result['url'] = link
    return result


def dailynews(link: str):
    source = 'dn'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    page = requests.get(link, headers=headers)
    content = page.content
    soup = BeautifulSoup(content, 'html.parser')
    heading = soup.find('h1').text
    ts = soup.find('span', class_='date').text
    ts = iso_date(ts)
    find_text = soup.find_all('div', class_='entry textbox content-all')
    text = ''
    for t in find_text:
        txt = t.text.strip()
        text += txt
    result = {}
    result['id'] = hashing(heading, source)
    result['ts'] = ts
    result['source'] = 'dailynews'
    result['heading'] = heading
    result['text'] = text
    result['url'] = link
    return result


def parse_news(url: str):
    sites_ls = ['thairath', 'dailynews', 'matichon', 'bangkokbiz', 'naewna']
    site = None
    for s in sites_ls:
        if re.search(s, url):
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


news = []
for url in urls:
    news_parsed = parse_news(url)
    if news_parsed != 'N/A':
        news.append(news_parsed)

with open('/temp/news_daily.json', 'w', encoding='utf-8') as f:
    json.dump(news, f, ensure_ascii=False)
