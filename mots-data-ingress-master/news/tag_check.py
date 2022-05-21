import json
import pandas as pd
import sys, os

os.chdir('E:/mots-data-ingress-master/news')
cwd = os.getcwd()
sys.path.append(cwd)

from news_func import *

with open('./gate1.json', encoding='utf-8') as f:
    gate1 = json.load(f)
with open('./gate2.json', encoding='utf-8') as f:
    gate2 = json.load(f)

func_call = {'thairath':thairath,
             'prachachat':prachachat,
             'posttoday':posttoday,
             'sanook':sanook,
             'manager':mgronline,
             'naewna':naewna,
             'dailynews':dailynews,
             'komchadluek':komchadluek,
             'standard': standard,
             'khaosod': khaosod,
             'matichon': matichon,
             'bkkbiz' : bkkbiz
}


tags_err = pd.read_excel('./tag_err.xlsx')

tags_col = []
tier_1 = []
tier_2 = []
for ind, val in tags_err.iterrows():
    link = val['link'].strip()
    src = val['source']
    print(link,src)
    ttags = []
    tt1 = []
    tt2 = []
    try:
        news = func_call[src](link)
        text = news['text']
        tags = gate(text,gate1,gate2)
        ttags.append(tags)
        for mstag, t1 in gate1.items():
            for i in t1:
                if i in text:
                    tt1.append(i)
                    for t2 in gate2[i]:
                        if t2 in text:
                            tt2.append(t2)
    except Exception as e:
        print(e)
        ttags.append('err')
        tt1.append('err')
        tt2.append('err')
    tags_col.append(ttags)
    tier_1.append(tt1)
    tier_2.append(tt2)


df_tag = pd.DataFrame.from_dict({'tags_col':tags_col,
                            'tier_1':tier_1,
                            'tier_2':tier_2})

# final
df_final = pd.concat([tags_err,df_tag],axis=1)
df_final.head()



df_final.to_excel('E:/mots-data-ingress-master/news/mislabeled_news.xlsx')
