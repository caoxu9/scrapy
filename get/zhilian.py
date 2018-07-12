'''
爬取智联招聘，ajax方式加载
'''
import requests,urllib3,json
from urllib.parse import urlencode

urllib3.disable_warnings()
def get_page(key,bb):
    url = 'https://fe-api.zhaopin.com/c/i/sou?'
    off = {
        'start':(int(bb)-1)*60,
        'pageSize':'60',
        'cityId':'530',
        'workExperience':'-1',
        'education':'-1',
        'companyType':'-1',
        'employmentType':'-1',
        'jobWelfareTag':'-1',
        'kw':key,
        'kt':'3',
    }
    headers = {
        'Host': 'fe-api.zhaopin.com',
        'Referer': 'https://sou.zhaopin.com/?jl=530&kw=Python&kt=3',
        'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/67.0.3396.18Safari/537.36',
    }
    new = url + urlencode(off)
    try:
        res = requests.get(new,headers=headers)
        # with open('c.txt','w',encoding='utf8') as f:
        #     f.write(res.text)
        return res.json()
    except requests.ConnectionError:
        return None
def get_data(json):
    li = []
    if json.get('data'):
        for item in json.get('data').get('results'):
            name = item.get('jobName')
            company = item.get('company').get('name')
            money = item.get('salary')
            type = item.get('company').get('type').get('name')
            li.append({'name':name,'company':company,'money':money,'type':type})
        return li

def save_page(item):
    with open('a.json','w',encoding='utf8')as f:
        json.dump(item,f)
def main():
    zz = input('请输入爬取的工作：')
    bb = input('请输入爬取的页数')
    a = get_page(zz,bb)
    b = get_data(a)
    save_page(b)
if __name__=='__main__':
    main()