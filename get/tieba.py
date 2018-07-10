'''
爬取百度贴吧图片
'''
import urllib.request
from urllib import parse
from lxml import etree
import os,random

class Spider:
    def __init__(self):
        self.tiebaname = input('输入要爬取的贴吧名：')
        self.beginpage = input('输入起始页码：')
        self.endpage = input('输入截止页码:')
        self.url = 'http://tieba.baidu.com/f'
        self.headers_list = [
            "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
            "Mozilla/5.0 (Macintosh; Intel Mac OS... "
        ]
        self.header = random.choice(self.headers_list)
        # # print(self.header)
        # self.http_proxy = urllib.request.ProxyHandler({'http':'159.38.62.107:9797'})
        # self.opener = urllib.request.build_opener(self.http_proxy)
        # # self.headers.add{'User-Agent':self.header}
        # urllib.request.install_opener(self.opener)
        # # print('++++++++++++++++++')
        self.username = 1
    def tiebaSpider(self):
        for i in range(int(self.beginpage),int(self.endpage)+1):
            pn = (i - 1)*50
            word = {'kw':self.tiebaname,'ie':'utf-8','pn':pn}
            myurl = self.url + '?'+urllib.parse.urlencode(word)
            self.loadpage(myurl)
    def loadpage(self,url):
        print(url)
        request = urllib.request.Request(url)
        request.add_header('User-agent',self.header)
        req = urllib.request.urlopen(request)
        # print(req.read().decode('utf8'))
        one = etree.HTML(req.read())
        links = one.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')
        for i in links:
            newurl = "http://tieba.baidu.com" + i
            self.writepage(newurl)
    def writepage(self,url):
        request = urllib.request.Request(url)
        request.add_headermei('User-Agent', self.header)
        html = urllib.request.urlopen(request)
        html = etree.HTML(html.read())
        links = html.xpath('//img[@class="BDE_Image"]/@src')
        for i in links:
            self.writeimage(i)
    def writeimage(self,url):
        print(url)
        print("正在存储文件 %d ..." % self.username)
        with open(str(self.username)+'.png','wb') as f:
            image = urllib.request.urlopen(url)
            f.write(image.read())
        self.username += 1
if __name__=='__main__':
    myspider=Spider()
    myspider.tiebaSpider()
