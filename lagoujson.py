'''
jsonpath爬取拉勾json
'''
import json
import jsonpath
import urllib.request

url = 'http://www.lagou.com/lbs/getAllCitySearchLabels.json'
request = urllib.request.Request(url)
req = urllib.request.urlopen(request)
# print(req.read().decode('utf8'))

#将json数据转换为 python数据
jsonobj = json.loads(req.read().decode('utf8'))
# print(jsonobj)

#匹配查找城市名
js = jsonpath.jsonpath(jsonobj,'$..name')
# print(js) 

将数据以json形式写入文档
with open('city.json','w',encoding='utf8') as f:
    content = json.dumps(js,ensure_ascii=False)
    # print(content)
    f.write(content)