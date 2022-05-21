from common import print_log
from configs import Config
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from models import Assignment as Assg, MasterTag as AssgMasterTag, AssignmentTag as AssgTag, AssignmentToLog as AssgLog


def get_assignment_tags() -> dict:
    """
    :return: { 'tag_name': (int) tag_id, ... }
    """
    tags: list[AssgMasterTag] = list(AssgMasterTag.select())
    tagsDict = dict()
    for t in tags:
        tagsDict[t.tag_name] = t.tag_id
    return tagsDict


def to_twitter_url(tw_src) -> str:
    return f'https://twitter.com/{tw_src.get("user").get("screen_name")}/status/{tw_src.get("id_str")}'


if __name__ == '__main__':
    es = Elasticsearch(Config.es_hosts, http_auth=(Config.es_http_user, Config.es_http_pwd), scheme="https", port=443)

    # only docs that have no 'x_elt_todb' field
    index = 'twitter-by-hashtags'
    body = {
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "bool": {
                            "must_not": [
                                {
                                    "exists": {
                                        "field": "x_etl_todb"
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    }
                ],
                "should": [],
                "must_not": []
            }
        }
    }
    docts = es.search(index=index, body=body)
    if len(docts.get('hits')['hits']) == 0:
        print_log('No new documents found in ES')
        exit(0)

    # Get Assignments Tag from DB
    masterTags = get_assignment_tags()

    now = datetime.now()
    cnt_new = 0
    cnt_err = 0
    for d in docts['hits'].get('hits'):

        try:
            src = d.get('_source')
            assg = Assg()
            assg.news_ref = d.get('_id')
            assg.news_name = src['full_text']
            assg.news_detail = src.get('full_text')
            assg.news_link = to_twitter_url(src)
            assg.news_source = 1 # Twitter
            assg.assign_to_permission = 1
            assg.asg_status = 10
            assg.is_active = 1
            assg.news_datetime = datetime.strptime(src.get('created_at'), '%a %b %d %H:%M:%S +0000 %Y') + timedelta(
                hours=7)
            assg.news_sync_datetime = now
            assg.save()

            for tashtag in src.get('entities').get('hashtags'):
                tagId = masterTags.get(tashtag['text'])
                if tagId:
                    assgTag = AssgTag()
                    assgTag.asg = assg.asg_id
                    assgTag.tag = tagId
                    assgTag.is_system = 1 # 1 = assign by system
                    assgTag.create_datetime = now
                    assgTag.is_active = 1
                    assgTag.save()

            assgLog = AssgLog()
            assgLog.asg_id = assg.asg_id
            assgLog.create_datetime = now
            assgLog.permission_id = 1
            assgLog.is_active = 1
            assgLog.is_finish = 0
            assgLog.is_over_duedate = 0
            assgLog.save()

            body = {
                "doc": {
                    "x_etl_todb": True
                }
            }
            es.update(index=index, id=d.get('_id'), body=body)

            cnt_new += 1
        except Exception as ex:
            if len(ex.args) > 1:
                if ex.args[0] == 1062: # DUPLICATE ERROR
                    body = {
                        "doc": {
                            "x_etl_todb": True
                        }
                    }
                    es.update(index=index, id=d.get('_id'), body=body)

            print_log(str(ex), 'ERROR')
            cnt_err += 1



    print_log(f'OK, Added:{cnt_new}, Error: {cnt_err}')
