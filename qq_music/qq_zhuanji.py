'''
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='u.y.qq.com', port=443): Max retries exceeded with url: /cgi-bin/musicu.fcg?callback=getUCGI19881362369113798&g_tk=5381&jsonpCallback=getUCGI19881362369113798&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22albumlib%22%3A%7B%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A14%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A520%2C%22num%22%3A20%2C%22click_albumid%22%3A0%7D%2C%22module%22%3A%22music.web_album_library%22%7D%7D (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x00000000049DE908>: Failed to establish a new connection: [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。',))
爬取3591个专辑后服务器断开
建议使用代理
爬取qq音乐的专辑，存入mongodb
'''
import requests,json
import time,random,datetime
from pymongo import MongoClient
from threading import Thread

mongo = MongoClient('mongodb://localhost:27017')
song_list = mongo['song']['song_list']
def qq_list(area,page):
    #爬取qq音乐专辑
    u = 'https://u.y.qq.com/cgi-bin/musicu.fcg?'
    callback = 'getUCGI'+str(random.random()).replace('0.','')
    param = 'callback={}&g_tk=5381&jsonpCallback={}&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22albumlib%22%3A%7B%22method%22%3A%22get_album_by_tags%22%2C%22param%22%3A%7B%22area%22%3A{}%2C%22company%22%3A-1%2C%22genre%22%3A-1%2C%22type%22%3A-1%2C%22year%22%3A-1%2C%22sort%22%3A2%2C%22get_tags%22%3A1%2C%22sin%22%3A{}%2C%22num%22%3A20%2C%22click_albumid%22%3A0%7D%2C%22module%22%3A%22music.web_album_library%22%7D%7D'.format(
        callback, callback, area, page * 20)
    url = u + param
    headers = {
        'authority': 'u.y.qq.com',
        'method': 'GET',
        'path': param,
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://y.qq.com/portal/album_lib.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    req = requests.get(url,headers=headers)
    time.sleep(1)
    body = json.loads(req.text.replace(callback,'').replace('(','').replace(')',''))
    list = body["albumlib"]["data"]["list"]
    for i in list:
        try:
            song_list.insert({'album_mid':i[ 'album_mid'],'album_name':i[ 'album_name'],'public_time':i['public_time']})
        except:
            print('hello')

if __name__ == '__main__':
    print('开始时间：',datetime.datetime.now())
    area = [0,1,3,4,14,15]
    try:
        threads = []
        for i in area:
            for j in range(1,30):
                a = Thread(target=qq_list,args=[i,j])
                a.start()
                threads.append(a)
        for i in threads:
                i.join()
    except:
        print('worry')
    print('结束时间：', datetime.datetime.now())