# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class MysecondcrawlPipeline(object):
    date_all = []

    def process_item(self, item, spider):
        data1=[]
        data1.append(dict(item))
        str1=item['commint_url'].replace('/','_').replace('https:__github.com','').lstrip()
        file1 = open(r'', 'w')#每次需要修改的地方，存放网页下载下来的文件的地址
        json.dump(data1, file1, indent=1)
        file1.close()
        print("数据存储完成！")
        return item

    def close_spider(self,spider):
        print("爬虫运行完了")
