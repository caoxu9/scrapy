'''
爬取今日头条
问题：sqlite3.OperationalError: near "美女图鉴": syntax error
'''
import requests,urllib3,sqlite3
from urllib.parse import urlencode,quote

urllib3.disable_warnings()
url = 'https://www.toutiao.com/search_content/?'
key = input('输入搜索关键字：')
ref = quote(key)
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.18Safari / 537.36',
    'Referer': 'https://www.toutiao.com/search/?keyword='+ref,
    'Cookie': 'csrftoken=a8f725e9486ecf0210a7cb1dbf27b041; tt_webid=6577249843588154883; UM_distinctid=1648dad69ba24d-0bd8229c5d53f9-6915147a-144000-1648dad69bc150; sso_login_status=0; tt_webid=6577249843588154883; WEATHER_CITY=%E5%8C%97%E4%BA%AC; CNZZDATA1259612802=1950324849-1531381788-https%253A%252F%252Fwww.toutiao.com%252F%7C1531621829; __tasessionId=t43sws8ob1531623067449',
}
count = input('输入数据量：')
conn = sqlite3.connect('daytiao.db')
cur = conn.cursor()
cur.execute('create table if not exists toutiao(title VARCHAR (255) NULL ,image VARCHAR (255) NULL,source VARCHAR (255) NULL)')
conn.commit()


#offset为0时数据不同，不作提取
for i in range(1,int(count)+1):
    offset = {
        'offset': i*20,
        'format': 'json',
        'keyword': key,
        'autoload': 'true',
        'count':'20',
        'cur_tab':'1',
        'from': 'search_tab',
    }
    myurl = url + urlencode(offset)
    req = requests.get(myurl,headers,verify=False)
    for i in req.json().get('data'):
        title = i.get('title')
        img = i.get('image_url')
        source = i.get('source')
        cur.execute('insert into toutiao(title,image,source) VALUES ("%s","%s","%s")'%(title,img,source))
        conn.commit()
conn.close()