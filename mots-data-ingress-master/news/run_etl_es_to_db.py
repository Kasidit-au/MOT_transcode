from common import print_log
from configs import Config
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from models import Assignment as Assg, MasterTag as AssgMasterTag, AssignmentTag as AssgTag, AssignmentToLog as AssgLog
import peewee


class Main(object):

    def __init__(self):
        pass


    def get_assignment_tags(self) -> dict:
        """
        :return: { 'tag_name': (int) tag_id, ... }
        """
        tags: list[AssgMasterTag] = list(AssgMasterTag.select())
        tagsDict = dict()
        for t in tags:
            tagsDict[t.tag_name] = t.tag_id
        return tagsDict


    def run(self):
        es = Elasticsearch(Config.es_hosts, http_auth=(Config.es_http_user, Config.es_http_pwd), scheme="https",
                           port=443)

        # only docs that have no 'x_elt_todb' field
        index = 'news-by-google'
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
        masterTags = self.get_assignment_tags()

        # Get Source Dict
        # ให้เอามาจาก Database แทน
        masterSources = {
            'nn': 6,
            'bb': 7,
            'dn': 8,
            'mc': 9,
            'tr': 10
        }

        now = datetime.now()
        cnt_new = 0
        cnt_err = 0
        for d in docts['hits'].get('hits'):

            try:
                src = d.get('_source')
                assg = Assg()
                assg.news_ref = d.get('_id')
                assg.news_name = src.get('heading')
                assg.news_detail = src.get('text')
                assg.news_link = src.get('url')
                assg.news_datetime = src.get('ts')
                assg.news_sync_datetime = now
                assg.assign_to_permission = 1
                assg.asg_status = 10
                assg.is_active = 1
                assg.news_source = masterSources.get(d.get('_id').split('-')[0])
                assg.save()

                if src.get('tag'):
                    for tashtag in src.get('tags'):
                        tagId = masterTags.get(tashtag)
                        if tagId:
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

                body = {
                    "doc": {
                        "x_etl_todb": True
                    }
                }
                es.update(index=index, id=d.get('_id'), body=body)
                cnt_new += 1
            except peewee.IntegrityError as ex:
                body = {
                    "doc": {
                        "x_etl_todb": True
                    }
                }
                es.update(index=index, id=d.get('_id'), body=body)
                cnt_err += 1
            except Exception as ex:
                print_log(str(ex), 'ERROR')
                cnt_err += 1

        print_log(f'OK, Added:{cnt_new}, Error: {cnt_err}')


if __name__ == '__main__':
    main = Main()
    main.run()
