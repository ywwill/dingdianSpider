# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdianItem(scrapy.Item):
    # define the fields for your item here like:

    name = scrapy.Field()

    author = scrapy.Field()

    novelurl = scrapy.Field()

    # 状态
    serialstatus = scrapy.Field()

    # 字数
    serialnumber = scrapy.Field()

    # 类别
    category = scrapy.Field()

    # 编号
    name_id = scrapy.Field()

class DcontentItem(scrapy.Item):
    # 小说编号
    id_name = scrapy.Field()

    # 章节内容
    chaptercontent = scrapy.Field()

    # 用于绑定章节顺序
    num = scrapy.Field()

    # 章节地址
    chapterurl = scrapy.Field()

    # 章节名字
    chaptername = scrapy.Field()
