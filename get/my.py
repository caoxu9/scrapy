'''
爬取猫眼电影数据
'''
import requests
from urllib.parse import urlencode
from pyquery.pyquery import PyQuery as pq
import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_url(key):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }
    url = 'https://maoyan.com/board/4?'
    offset = {'offset':key*10}
    # offset = {'offset':20}
    myurl = url + urlencode(offset)
    req = requests.get(myurl,headers=headers)
    # print(req.text)
    return req.text
def save_page(text):
    html = pq(text)
    engine =create_engine("mysql://root:123456@localhost/scrapy?charset=utf8",encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in range(len(html('dd'))):
        fname = html('dd p a')[i].text
        start = html('.star')[i].text
        ftime = html('.releasetime')[i].text
        session.execute("INSERT INTO maoyan(fname,star,ftime) VALUES ('%s','%s','%s')"%(fname,start,ftime))
        session.commit()
    session.close()
def main():
    page = input('输入爬取到的页数:')
    for i in range(int(page)):
        p = get_url(i)
        save_page(p)
if __name__=="__main__":
    main()