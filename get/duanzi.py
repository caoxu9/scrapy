'''
使用lxml抓取糗事百科的博主发表的文章、姓名和头像
'''
import json
import urllib.request
from urllib import parse
import random
from lxml import etree

headers_list = [
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... ",
]
header = random.choice(headers_list)
beginpage = input('输入起始页')
endpage = input('结束页')
filename = 1
url = 'https://www.qiushibaike.com/8hr/page'
for i in range(int(beginpage),int(endpage)+1):
    myurl = url +'/'+str(i)
    request = urllib.request.Request(myurl)
    request.add_header('User-Agent',header)
    html = urllib.request.urlopen(request)
    one = etree.HTML(html.read())
    list = one.xpath('//a[@class="contentHerf"]/@href')
    ls = []
    for j in list:
        newurl = 'https://www.qiushibaike.com'+j
        request = urllib.request.Request(newurl)
        request.add_header('User-Agent',header)
        req = urllib.request.urlopen(request)
        html = etree.HTML(req.read())
        li = html.xpath("//div[@class='content']")
        lp = html.xpath("//div[@class='author clearfix']//img/@src")
        ln = html.xpath("//div[@class='author clearfix']//img/@alt")
        for i in range(len(lp)):
            ls.append({'name':ln[i],'img':lp[i],'comment':li[i].text})
a = json.dumps(ls)
with open('a.json','w')as f:
    f.write(a)
