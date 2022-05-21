import tweepy
from common import print_log
from configs import Config
from elasticsearch import Elasticsearch
from models import MasterTag
from typing import List


if __name__ == '__main__':
    try:
        auth = tweepy.OAuthHandler(Config.consumer_key, Config.consumer_secret)
        auth.set_access_token(Config.access_tokne, Config.access_token_secret)

        api = tweepy.API(auth)

        # GET Master Tags
        tags: List[MasterTag] = list(MasterTag.select().where(MasterTag.is_active == 1))
        if len(tags) == 0:
            print_log('No obtained tags from database')
            exit(0)

        # [REF: Twitter Search Format] https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
        # [REF: api.search] https://docs.tweepy.org/en/latest/api.html#search-methods
        # [REF: filter] https://stackoverflow.com/questions/27941940/how-to-exclude-retweets-and-replies-in-a-search-api
        # q = '#อุบัติเหตุ'
        q = '('
        tags_cnt = len(tags[0:20])
        for i in range(tags_cnt):

            # ถ้าคำมี เว้นวรรค ให้ครอบด้วย quote
            if len(tags[i].tag_name.strip().split(' ')) > 1:
                tags[i].tag_name = '"' + tags[i].tag_name + '"'

            q += f'#{tags[i].tag_name} '
            if i != tags_cnt - 1:
                q += 'OR '

        filter = ') AND -filter:retweets'
        q += filter
        tweets = api.search(q, lang='th', result_type='recent', tweet_mode='extended')

        es = Elasticsearch(Config.es_hosts, http_auth=(Config.es_http_user, Config.es_http_pwd), scheme="https", port=443)
        for tw in tweets:

            tw.id_str = 'tw-' + tw.id_str
            tw_data = tw._json
            tw_data['x_search_by'] = 'hashtag'
            es.index(index='twitter-by-hashtags', id=tw.id_str, body=tw_data)

        print_log(f'OK: {len(tweets)} tweets')

    except Exception as err:
        print_log(str(err))
