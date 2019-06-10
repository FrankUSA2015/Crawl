# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MysecondcrawlItem(scrapy.Item):
    # 存放修改的代码和没有修改的代码
     add_code = scrapy.Field()
     delect_code = scrapy.Field()
     postion_code = scrapy.Field()


class commintItem(scrapy.Item):
    #存放每个commint对应的title，desc，doc
     commint_title = scrapy.Field()
     commint_desc = scrapy.Field()
     commint_doc = scrapy.Field()
     commint_url = scrapy.Field()
     possible_error_doc = scrapy.Field()

