# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class ZhilianPipeline(object):
    def __init__(self):
        self.engine =create_engine("mysql://root:123456@localhost/scrapy?charset=utf8",encoding='utf8')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    def process_item(self, item, spider):
        sql = "insert into zhilian(gongzuo,company,money,ty,statu) values ('%s','%s','%s','%s','%s')"%(item['gongzuo'],item['company'],item['money'],item['ty'],item['statu'])
        self.session.execute(sql)
        self.session.commit()
    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.session.close()
# class MysqlPipeline():
#     def __init__(self,host,database,user,password,port):
#         self.host = host
#         self.database = database
#         self.user = user
#         self.password = password
#         self.port = port
#     def open_spider(self,spider):
#         self.db = pymysql.connect(self.host,self.port,self.user,self.password,self.database,charset='utf8')
#         self.cursor = self.db.cursor()
#     def close_spider(self,spider):
#         self.db.close()
#     def process_item(self,item,spider):
#         data = dict(item)
#         keys = ','.join(data.keys())
#         values = ','.join(['%s']*len(data))
#         sql = 'insert into %s (%s) VALUES (%s)'%()


