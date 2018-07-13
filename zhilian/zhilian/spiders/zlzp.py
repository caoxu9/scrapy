# -*- coding: utf-8 -*-
import scrapy,json
import urllib3
from .. import items
from urllib.parse import urlencode
from pyquery.pyquery import PyQuery as pq
urllib3.disable_warnings()


class ZlzpSpider(scrapy.Spider):
    name = 'zlzp'
    allowed_domains = ['zhaopin.com']
    url = 'https://fe-api.zhaopin.com/c/i/sou?'
    off = {
        'start': '0',
        'pageSize': '60',
        'cityId': '530',
        'workExperience': '-1',
        'education': '-1',
        'companyType': '-1',
        'employmentType': '-1',
        'jobWelfareTag': '-1',
        'kw': 'python',
        'kt': '3',
    }
    start_urls = [url+urlencode(off)]
    def parse(self, response):
        data = json.loads(response.body)
        item = items.ZhilianItem()
        for i in data.get('data').get('results'):
            item['company'] = i.get('company').get('name')
            item['gongzuo'] = i.get('jobName')
            item['money'] = i.get('salary')
            item['ty'] = i.get('company').get('type').get('name')
            item['statu'] = i.get('timeState')
            item['id'] = i.get('company').get('id')
            yield item

