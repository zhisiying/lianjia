# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst
class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:

    out_put = scrapy.Field(output_processor=TakeFirst())
    url = out_put
    楼盘名  = out_put
    开盘时间 = out_put
    开发商= out_put
    物业类型 = out_put
    参考价格 = out_put
    项目特色 = out_put
    区域位置 = out_put
    楼盘地址 = out_put
    售楼处地址 = out_put
    建筑类型 = out_put
    绿化率 = out_put
    占地面积 = out_put
    容积率 = out_put
    建筑面积 = out_put
    产权年限 = out_put
    楼盘户型 = out_put
    物业公司 = out_put
    车位配比= out_put
    物业费 = out_put
    供暖方式 = out_put
    供水方式 = out_put
    供电方式 = out_put
    车位 = out_put

