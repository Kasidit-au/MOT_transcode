import requests
from datetime import datetime
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
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from models import *
import peewee
from peewee import *
import json

db = MySQLDatabase('mots-dev', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': 'mots-mariadb.mariadb.database.azure.com', 'port': 3306, 'user': 'xphys@mots-mariadb', 'password': 'ItsInternet'})

result = (MasterSource
          .insert(source_id='16', source_name='mgr')
          .on_conflict('replace')
          .execute())

