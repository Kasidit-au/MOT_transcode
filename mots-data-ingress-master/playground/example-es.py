from elasticsearch import Elasticsearch
from datetime import datetime

if __name__ == '__main__':
    es = Elasticsearch(
        ['https://144affa021204e0b8ac9db0d13933bd8.southeastasia.azure.elastic-cloud.com:9243'],
        http_auth=('elastic', 'u0CWdX9NocEf7NAhfLRMTm8J'),
        scheme="https", port=443, )

    # Data (Dict, Json)
    data = {
        'author': 'Au',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'my_ts': datetime.now(),
    }

    # "index" ===> "database"
    # "data-type" ===> "table" (optional)
    # "body" ===> "document" "record"
    es.index(index="my-index", id='dsadsadsadasdas', body=data)

    print('OK')