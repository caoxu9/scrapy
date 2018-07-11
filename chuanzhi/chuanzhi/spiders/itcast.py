'''
使用scrapy爬取传智教师信息并存储为json格式
'''
# -*- coding: utf-8 -*-
import scrapy
from .. import items

class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml",]

    def parse(self, response):
        li = []
        for i in response.xpath("//div[@class='li_txt']"):
            item = items.ChuanzhiItem()
            name = i.xpath("h3/text()").extract()
            title = i.xpath("h4/text()").extract()
            info = i.xpath("p/text()").extract()
            item['name'] = name[0]
            item['level'] = title[0]
            item['info'] = info[0]
            li.append(item)
        return li
