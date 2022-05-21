import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly
from plotly.graph_objs import Scatter, Layout,Line
pd.set_option('display.max_columns',100)
# import data
df = pd.read_csv('E:\HTOC\doh-sensor.agg_1h_2020_10.csv')
df.columns
len(df)
df.dtypes
len(df['device_code'].unique())

df['device_code'].isnull().sum()
df[df['device_code'] == np.nan]

# change to datetime
df['created_datetime'] = pd.to_datetime(df['created_datetime'])
df['sensor_datetime'] = pd.to_datetime(df['sensor_datetime'])

# drop test 1234
df_test = df[df['device_code'] == 'TEST1234']
df = df[df['device_code'] != 'TEST1234']
df['loc'] = df['device_code'].astype(str).apply(lambda x:x[0:14])

# merge with lagkilo data
# lagkilo data
df_lagkilo = pd.read_csv('G:\My Drive\colored\km_n_newlag.csv',sep=';')
#
df['km_label'] = df['loc'].apply(lambda x:x[5:9].lstrip('0'))+'+'+\
                 df['loc'].apply(lambda x:x[9:12])+\
                 '('+df['loc'].apply(lambda x:x[0:4])+')'
#
df['km_label'] = df['loc'].apply(lambda x:x[5:9].lstrip('0'))+'+000'+\
                 '('+df['loc'].apply(lambda x:x[0:4])+')'
                 # df['loc'].apply(lambda x:x[9:12])+\
df['km_label'].unique()
#
df_processed = pd.merge(df, df_lagkilo, how="left", on="km_label")
df_processed.dropna(inplace=True)

df_processed['km_label'].unique()

df_processed.to_excel('E:/HTOC/df_processed.xlsx')
# unique loc
loc_unique = df['loc'].unique()

df3['sensor_datetime'].unique()

for l in loc_unique[:2]:
    df2 = df[df['loc'] == l]
    df3 = df2[(df2['sensor_datetime'] >= '2020-05-10') & (df2['sensor_datetime'] <= '2020-05-11')]
    figure = plt.figure()
    for i in range(0, 4):
        df_ = df3[df3['lane'] == i]
        plt.plot(df_['sensor_datetime'], df_['avg_speed'], label=f'Lane {i}')
    df_avg_lanes = df3.groupby(['sensor_datetime']).mean('avg_speed')
    plt.plot(df_avg_lanes.index, df_avg_lanes['avg_speed'], label='all', color='r')
    plt.title(f'Average Speed per time for {l}')
    plt.xlabel('time')
    plt.ylabel('Average Speed')
    plt.legend()
    plt.show()


##### speed in each each lagkilo

# plot some graph
# plt.plot(df2['sensor_datetime'],df2['avg_speed'])
# figure = plt.figure(figsize=(10,3))

# df3 = df2.iloc[:,0:100]




for i in range(0,5):
    df4[df4['lane'] == i].plot(kind='scatter',
        x = 'sensor_datetime', y = 'avg_speed',title = f'Average Speed against time {i}',ylabel='Average Speed')

df4[df4['lane'] == 1].plot(
        x = 'sensor_datetime', y = 'avg_speed',title = 'Average Speed against time',ylabel='Average Speed'
    )

# groupby one day
df_one_day = df2.groupby(pd.Grouper(key="sensor_datetime",freq='1H')).mean('speed')
df2.dtypes

plt.plot(df_one_day.index,df_one_day['avg_speed'])


# plotly

plotly.offline.plot({
    "data": [(x=df3['sensor_datetime'], y=df3['avg_speed'])],
    "layout": Layout(title="Avg Speed")
})


plotly.offline.plot({
    "data": [(x=df_one_day.index, y=df_one_day['avg_speed'].values)],
    "layout": Layout(title="Avg Speed")
})

