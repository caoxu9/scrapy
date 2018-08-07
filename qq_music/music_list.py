'''
从mongodb中读取专辑的url，发送请求获取歌曲的url，然后存入数据库
歌曲为42406首
时间
2018-08-07 10:43:34.790116   开始时间
2018-08-07 10:45:18.966075   结束时间
'''

import requests,json
import time,random,datetime
from pymongo import MongoClient
from pyquery.pyquery import PyQuery as pq
from threading import Thread

mongo = MongoClient('mongodb://localhost:27017')

song_list = mongo['song']['song_list']
def song(i):
    #爬取专辑对应歌曲的url
    music_list = mongo['song']['music_list']
    url = 'https://y.qq.com/n/yqq/album/'+i+'.html'
    headers = {
        'authority': 'y.qq.com',
        'method': 'GET',
        'path': '/n/yqq/album/'+i+'.html',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache - control': 'max - age = 0',
        'referer': 'https://y.qq.com/portal/album_lib.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    req = requests.get(url,headers=headers)
    time.sleep(1)
    html = pq(req.text)('.songlist__songname_txt a').items()

    for a in html:
        try:
            music_list.insert({'music_add':a.attr('href'),'music_name':a.text()})
        except:
            print('worry')
if __name__ == '__main__':
    print(datetime.datetime.now())
    try:
        threads = []
        for i in song_list.find():
            a = Thread(target=song,args=[i['album_mid']])
            a.start()
            threads.append(a)
        for i in threads:
            i.join()
    except:
        print('worry')
    print(datetime.datetime.now())
