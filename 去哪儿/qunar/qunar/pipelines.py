# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

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
