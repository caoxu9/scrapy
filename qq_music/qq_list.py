'''
爬取qq音乐专辑信息
'''
import requests,json
import time,random,pymysql
from pyquery.pyquery import PyQuery as pq

connect = pymysql.connect(host='localhost',port=3306,user='root',password='123456',database='uplooking')
con = connect.cursor()
# con.execute('create table if not exists qq_list(album_mid varchar(256) not null ,album_name varchar(256) not null,public_time varchar(256) not null)')
# con.execute('create table if not exists music_list(music_add varchar(256) not null ,music_name varchar(256) not null)')
con.execute('create table if not exists song(name varchar(256) not null ,songer varchar(256) not null)')
# connect.commit()
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
    body = json.loads(req.text.replace(callback,'').replace('(','').replace(')',''))
    list = body["albumlib"]["data"]["list"]
    for i in list:
        con.execute('insert into qq_list(album_mid,album_name,public_time) values ("%s","%s","%s")'%(i[ 'album_mid'],i[ 'album_name'],i['public_time']))
    connect.commit()

def song_list():
    #爬取专辑对应歌曲的url
    con.execute('select album_mid from qq_list')
    for i in con.fetchall():
        i= str(i).replace('(','').replace(')','').replace(',','').replace("'",'')
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
            con.execute('insert into music_list(music_add, music_name) values ("%s","%s")' % (a.attr('href'),a.text()))
        connect.commit()


def song():
    con.execute('select music_add from music_list')
    for i in con.fetchall():
        i = str(i).replace('(', '').replace(')', '').replace("'", '')
        url = 'https:'+ i
        j = i.split('/')[-1]
        headers = {
            'authority': 'y.qq.com',
            'method': 'GET',
            'path': '/n/yqq/song/' + str(j),
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache - control': 'max - age = 0',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        req = requests.get(url,headers=headers)
        time.sleep(1)
        song_name = pq(req.text)('.data__name_txt').text()
        song_singer = pq(req.text)('.data__singer').text()
        con.execute('insert into song (name,singer) values ("%s","%s")'%(song_name,song_singer))
        connect.commit()
if __name__ == '__main__':

    #area为音乐的区域
    area = [1,0,3,15,14,4]
    for i in area:
        #j是爬取音乐的页数
            for j in range(5):
                try:
                    #生成专辑列表
                    qq_list(i,j)
                except:
                    print('worry')
    #生成歌曲的url
    song_list()


    #爬取歌曲的歌曲名和作者
    song()
connect.close()

