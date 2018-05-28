# -*- coding: utf-8 -*-
import scrapy
import math
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from bs4 import BeautifulSoup
from lianjia.items import LianjiaItem
from scrapy.loader import ItemLoader


class LinajiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.fang.lianjia.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="fc-main clear"]/div/ul/li/div//a'), callback='parse_item',
             follow=True, ),
    )

    def parse_item(self, response):
        city_url = response.urljoin('/loupan/')
        yield Request(city_url, callback=self.city_Item, dont_filter=True, )

    def city_Item(self, reseponse):
        loupan = reseponse.xpath('/html/body/div[5]/@data-total-count')[0].extract()
        num = math.ceil(int(loupan) / 10)
        louoan_urls = [reseponse.url + 'pg%s/' % i for i in range(1, num)]
        for i in louoan_urls:
            yield Request(i, callback=self.loupans_Item, dont_filter=True)

    def loupans_Item(self, reseponse):
        list_url = reseponse.xpath('//ul[@class="resblock-list-wrapper"]/li/a/@href').extract()
        for i in list_url:
            url1 = reseponse.urljoin(i)
            url2 = url1 + 'xiangqing/'
            yield Request(url2, callback=self.loupan_Item, dont_filter=True)
    

    def loupan_Item(self, reseponse):
        bs4 = BeautifulSoup(reseponse.text, 'lxml')
        loader = ItemLoader(item=LianjiaItem(), reseponse=reseponse)
        title = reseponse.xpath('//div[@class="fl l-txt"]/a[5]/@title').extract_first()
        time = reseponse.xpath('//ul[2]/li[2]/span[1]/span/text()').extract_first()
        xinxi_a = bs4.find('div', class_="big-left fl")
        xinxi1 = xinxi_a.select('ul.x-box')[0]
        xinxia = xinxi1.select('li > span.label-val')
        leixin = xinxia[0].text
        price = xinxia[1].text.split()[1]
        tese = xinxia[2].text
        area = xinxia[3].text
        location = xinxia[4].text
        shoulou_ld = xinxia[5].text
        kfs = reseponse.xpath('//div[1]/ul[1]/li[7]/span[2]/text()').extract_first()
        xinxi2 = xinxi_a.select('ul.x-box')[1]
        xinxib = xinxi2.select('li > span.label-val')
        jz_type = xinxib[0].text
        lvhualv = xinxib[1].text
        zdmj = xinxib[2].text.split()
        rongjilv = xinxib[3].text
        jzmj = xinxib[4].text.split()
        ghus = xinxib[6].text
        cqnx = xinxib[7].text
        lphx = ''.join(xinxib[8].text.split())
        xinxi3 = xinxi_a.select('ul.x-box')[2]
        xinxic = xinxi3.select('li > span.label-val')
        wygs = xinxic[0].text
        cwpv = xinxic[1].text
        wyf = xinxic[2].text.split()
        gnfs = xinxic[3].text
        gsfs = xinxic[4].text.split()
        gdfs = xinxic[5].text
        cws = xinxic[6].text.split()
        loader.add_value('url', reseponse.url)
        loader.add_value('楼盘名', title)
        loader.add_value('开盘时间', time)
        loader.add_value('物业类型', leixin)
        loader.add_value('区域位置', area)
        loader.add_value('楼盘地址', location)
        loader.add_value('售楼处地址', shoulou_ld)
        loader.add_value('开发商', kfs)
        loader.add_value('建筑类型', jz_type)
        loader.add_value('绿化率', lvhualv)
        loader.add_value('占地面积', zdmj)
        loader.add_value('容积率', rongjilv)
        loader.add_value('建筑面积', jzmj)
        loader.add_value('产权年限', cqnx)
        loader.add_value('楼盘户型', lphx)
        loader.add_value('物业公司', wygs)
        loader.add_value('车位配比', cwpv)
        loader.add_value('物业费', wyf)
        loader.add_value('供暖方式', gnfs)
        loader.add_value('供水方式', gsfs)
        loader.add_value('供电方式', gdfs)
        loader.add_value('车位', cws)
        yield loader.load_item()
        print(loader.load_item())
