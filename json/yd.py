'''
有道翻译在页面中用js进行数据加密
页面中的salt和sign为加密数据
D = "ebSeFb%=XZ%T[KZ)c(sy!",
S = 'fanyideskweb'
salt: r,
sign: o,
n = 要翻译文件
r = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10)),
o = u.md5(S + n + r + D),
'''
import requests,math,time,random,hashlib
from urllib.parse import urlencode


url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
headers = {
    'Referer': 'http://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=1453960131@114.245.42.161; OUTFOX_SEARCH_USER_ID_NCOO=9763099.044466363; fanyi-ad-id=46607; fanyi-ad-closed=1; JSESSIONID=aaaHZgx5sTXzn6I11VTsw; ___rl__test__cookies=1531923368251',
}
key = input('输入')
s = 'fanyideskweb'
d = "ebSeFb%=XZ%T[KZ)c(sy!"
r = str(int(time.time()*1000) + random.randint(1,10))
sign = hashlib.md5((s+key+r+d).encode('utf8')).hexdigest()
data = {
    'i': key,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': r,
    'sign': sign,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTIME',
    'typoResult': 'false',
}
req = requests.post(url,headers=headers,data=data)
a = req.json().get('translateResult')[0][0].get('tgt')
print(a)