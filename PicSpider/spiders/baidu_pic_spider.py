# -*- coding: utf-8 -*-

import scrapy, json
from scrapy.http import Request
from PicSpider.items import PicItem  # 导入item


class PicSpider(scrapy.Spider):
    name = "pic_spider"
    allowed_domains = ["http://image.baidu.com/"]
    start_urls = ["http://image.baidu.com"]

    def parse(self, response):  # 定义解析函数
        search_word = '哈士奇'  # 查找词，可修改
        baidu_pic_url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={0}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=60&rn=30&gsm=3c&1507915209449=".format(
            search_word)  # 百度图片url

        # 将带关键词参数的url交给request函数解析，返回的response通过get_pic回调函数进一步分析
        yield Request(baidu_pic_url, meta={"search_word": search_word}, callback=self.get_pic, dont_filter=True)

    def get_pic(self, response):  # 从图片list中获取每个pic的信息

        item = PicItem()  # 实例化item
        response_json = response.text  # 存储返回的json数据
        response_dict = json.loads(response_json)  # 转化为字典
        response_dict_data = response_dict['data']  # 图片的有效数据在data参数中

        for pic in response_dict_data:  # pic为每个图片的信息数据，dict类型
            if pic:
                item['search_word'] = response.meta['search_word']  # 搜索关键词赋值
                item['pic_url'] = [pic['middleURL']]  # 百度图片搜索结果url (setting中pic_url应该为数组形式)
                item['pic_name'] = pic['fromPageTitleEnc']  # 百度图片搜索结果对应的title
                yield item
