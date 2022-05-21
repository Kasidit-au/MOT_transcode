import os
import json
from elasticsearch import Elasticsearch
from common import print_log
from configs import Config

if __name__ == '__main__':

    with open('/temp/rss_feed_news.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    # ES
    index = 'news-by-google'

    es = Elasticsearch(Config.es_hosts, http_auth=(Config.es_http_user, Config.es_http_pwd), scheme="https", port=443)
    cnt_add = 0
    for r in results:
        if isinstance(r, dict):
            r['x_search_by'] = 'google'
            es.index(index=index, id=r['id'], body=r)
            cnt_add += 1

    print_log(f'OK: {cnt_add} news')
