# -*- coding: utf-8 -*-

import scrapy

class PicItem(scrapy.Item) :
    search_word = scrapy.Field() #搜索关键字
    pic_name = scrapy.Field() #图片标题
    pic_url = scrapy.Field() #图片url
    pass

