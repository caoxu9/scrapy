'''
使用bs4爬取腾讯社招
'''
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
import random
url = 'http://hr.tencent.com/position.php?keywords=&lid=0&start='
headers_list = [
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... ",
]
headers = random.choice(headers_list)
startpage = input('输入起始页:')
endpage = input('输入截止页:')
for i in range(int(startpage),int(endpage)+1):
    myurl = url + str(10*(i-1)) +'#a'
    request = urllib.request.Request(myurl)
    request.add_header('User-Agent',headers)
    req = urllib.request.urlopen(request)
    soup = BeautifulSoup(req.read().decode('utf8'),'lxml')
    li = soup.select('tr[class="even"] a')
    for i in li:
        newurl = 'https://hr.tencent.com/' + str(i['href'])
        request = urllib.request.Request(newurl)
        request.add_header('User-Agent',headers)
        re = urllib.request.urlopen(request)
        # print(re.read())
        scs = BeautifulSoup(re.read().decode('utf8'),'lxml')

        #爬取详细介绍
        li = scs.select('tr[class="c"]')

        #爬取职位
        ls = scs.select('tr[class="h"]')

        
        #爬取地点、类别、人数
        lc = scs.select('tr[class="c bottomline"] td')
        for i in ls:
            print(i.get_text())
        for i in lc:
            print(i.get_text())
        for i in li:
            print(i.get_text())   
