# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from twisted.enterprise import adbapi
import copy
import pymysql
from scrapy.utils.project import get_project_settings

class QunarPipeline(object):
    def process_item(self, item, spider):
        return item


class PipelineToJson(object):
    def __init__(self):
        # 设置保存文件名字
        self.f = open('city_list.json','w')

    def process_item(self, item, spider):
        # 通过json包将item转换成“{name:value}”这种格式
        content = json.dumps(dict(item),ensure_ascii = False) + ',\n'
        self.f.write(content)
        return item

    def colse_spider(self, spider):
        # 关闭流
        self.f.close()

class PipelineToMysql(object):
    def __init__(self):
        # 设置连接数据库参数
        settings = get_project_settings()
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接数据库
        self.post = adbapi.ConnectionPool('pymysql',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....

    def process_item(self, item, spider):
        # 深拷贝
        cityItem = copy.deepcopy(item)
        # 保存数据
        query = self.post.runInteraction(self._conditional_insert, cityItem)
        # 保存失败调用
        # query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tb, item):
        '''
        数据持久化
        '''
        sql = "insert into qunar_city (name, url) values (%s, %s)"
        params = (item["name"], item["url"])
        tb.execute(sql, params)