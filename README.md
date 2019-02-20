# Baidu-pic-spider

###### 安装scrapy
```pip install Scrapy ```

###### 进入终端，切换到自己项目代码的工作空间下，执行
```scrapy startproject baidu_pic_spider```

![image.png](https://upload-images.jianshu.io/upload_images/1731341-506b0b8a62b2f62b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


###### 生成如下工程文件：
images是自己创建的用于存放爬到的图片目录。

![image.png](https://upload-images.jianshu.io/upload_images/1731341-9b6763e7255ed1db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
在spiders目录下创建baidu_pic_spider爬虫文件，search_word可改成自己需要的搜索词。
 
##### baidu_pic_spider.py
```
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
```

新建main.py文件，方便在pycharm中运行和调试爬虫。
##### main.py

```
# _*_ coding: utf-8 _*_

from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))) #设置工程目录
print(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","pic_spider"]).strip()
```
定义item字段
##### item.py
```
# -*- coding: utf-8 -*-

import scrapy

class PicItem(scrapy.Item) :
    search_word = scrapy.Field() #搜索关键字
    pic_name = scrapy.Field() #图片标题
    pic_url = scrapy.Field() #图片url
    pass

```
定义pipeline
##### pipeline.py
```
# -*- coding: utf-8 -*-


class PicspiderPipeline(object):
    def process_item(self, item, spider):
        return item


```
在setting中对应部分修改ITEM_PIPELINES，并增加图片处理代码
##### settings.py
```
ITEM_PIPELINES = {

    'PicSpider.pipelines.PicspiderPipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline' : 1,
}
#配置pipeline，设定需要进行处理的图片路径
IMAGES_URLS_FIELD = "pic_url"
# 设置图片下载后的存储路径，放到工程目录下images文件夹
# 获取当前目录绝对路径
project_dir = os.path.abspath(os.path.dirname(__file__))
# 获取images存储路径
IMAGES_STORE = os.path.join(project_dir,'images')

# 设定处理图片的最小高度，宽度
IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100
```

#### 运行
```run main.py```

![image.png](https://upload-images.jianshu.io/upload_images/1731341-0c1a4367ba1c514c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
