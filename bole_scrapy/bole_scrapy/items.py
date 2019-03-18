# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.Item):
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    article_image_url = scrapy.Field()
    article_image_local_path = scrapy.Field()
    article_date = scrapy.Field()
    article_tag = scrapy.Field()
    article_like_num = scrapy.Field()
    article_collect = scrapy.Field()
    article_comment = scrapy.Field()
