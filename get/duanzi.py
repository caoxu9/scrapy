'''
使用lxml抓取糗事百科的博主发表的文章、姓名和头像
'''
import os
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
    for j in list:
        newurl = 'https://www.qiushibaike.com'+j
        request = urllib.request.Request(newurl)
        request.add_header('User-Agent',header)
        req = urllib.request.urlopen(request)
        html = etree.HTML(req.read())
        li = html.xpath("//div[@class='content']")
        lp = html.xpath("//div[@class='author clearfix']//img/@src")
        ln = html.xpath("//div[@class='author clearfix']//img/@alt")
        for m in lp:
            nurl = 'http:'+m
            request = urllib.request.Request(nurl)
            request.add_header('User-Agent',header)
            req = urllib.request.urlopen(request)
            with open(str(filename)+'.png','wb') as f:
                f.write(req.read())
        for i in ln:
            with open(str(filename)+'.txt','w',encoding='utf8') as f:
                f.write(i)
        with open(str(filename)+'.doc','w',encoding='utf8') as f:
            f.write(li[0].text)
        filename += 1
        
        
        
