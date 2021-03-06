'''
爬取拉钩网站招聘数据
'''
import requests,urllib3,MySQLdb,datetime,sqlite3,time
from urllib.parse import urlencode


urllib3.disable_warnings()
url = 'https://www.lagou.com/jobs/positionAjax.json?'
key = input('输入要爬取的数据：')
page = input('输入爬取的数据量（页数）:')
city = input('输入城市：')
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
offset = {
    'city':city,
    'needAddtionalResult':'false',
}

#请求头需要有cookie,uer-agent,referer
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.18Safari / 537.36',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'Cookie': 'JSESSIONID=ABAAABAAAIAACBI5867007E35E92110F4C4FAA7D9850FFB; _ga=GA1.2.1190351284.1531578497; _gid=GA1.2.2007515560.1531578497; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531578497; user_trace_token=20180714222823-2a1ea2a6-8772-11e8-9a3d-525400f775ce; LGSID=20180714222823-2a1ea414-8772-11e8-9a3d-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DHxkNvh3Ux7pUsH6Fn5HNZdiQMw-h1UPQUoUDF0fY9Pa%26wd%3D%26eqid%3Db1f1282d0001b46e000000035b4a087b; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180714222823-2a1ea5c0-8772-11e8-9a3d-525400f775ce; TG-TRACK-CODE=search_code; X_HTTP_TOKEN=e27fb23764504e242ceacbe33f681786; LG_LOGIN_USER_ID=f4aa006e0679d8b6093bd399b99b89036dd424bb0dd26061; _putrc=2EBFCA71673909E1; login=true; unick=%E6%9B%B9%E6%97%AD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; _gat=1; gate_login_token=7f40457d684a272239b8d42f5958112a75373a781d76b067; SEARCH_ID=a07d4c3b384b4fcf91e7fcdd2babca25; index_location_city=%E5%8C%97%E4%BA%AC; LGRID=20180714223540-2e87920f-8773-11e8-9dec-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1531578935',
}
conn = sqlite3.connect('lagou.db')
cur = conn.cursor()
cur.execute('create table if not exists lagou(positionname VARCHAR(255) NULL,workyear VARCHAR(255) NULL,education VARCHAR(255) NULL,salary VARCHAR(255) NULL,companyfullname VARCHAR(255) NULL,formatcreatetime VARCHAR(255) NULL)')
conn.commit()

#首页
data = {
        'first': 'true',
        'pn': "1",
        'kd': key,
    }
time.sleep(1)
myurl = url + urlencode(offset)
req = requests.post(myurl, headers=headers, data=data)
li = req.json().get('content').get('positionResult').get('result')
conn = sqlite3.connect('lagou.db')
cur = conn.cursor()
for i in li:
    cur.execute(
        'insert into lagou(positionname,workyear,education,salary,companyfullname,formatcreatetime) VALUES ("%s","%s","%s","%s","%s","%s")' % (i['positionName'], i['workYear'], i['education'], i['salary'], i['companyFullName'], i['formatCreateTime']))
    conn.commit()

#获取之后页面
if int(page)>1:
    for i in range(2,int(page)+1):
        time.sleep(1)
        data = {
            'first': 'false',
            'pn': i,
            'kd': key,
        }
        myurl = url + urlencode(offset)
        req = requests.post(myurl,headers=headers,data=data)
        li = req.json().get('content').get('positionResult').get('result')
        conn = sqlite3.connect('lagou.db')
        cur = conn.cursor()
        for i in li:
            cur.execute('insert into lagou(positionname,workyear,education,salary,companyfullname,formatcreatetime) VALUES ("%s","%s","%s","%s","%s","%s")'%(i['positionName'],i['workYear'],i['education'],i['salary'],i['companyFullName'],i['formatCreateTime']))
            conn.commit()
conn.close()
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
