# -*- coding: utf-8 -*-
import scrapy
from MovieSpider.items import MoviespiderItem

class Move250Spider(scrapy.Spider):
    name = 'move250'
    allowed_domains = ['movie.douban.com']

    #偏移量
    offset = 0
    url = "https://movie.douban.com/top250?start="
    start_urls = [url+str(offset)+"&filter="]

    # start_urls = ["http://118.190.202.67:8000/test/"]


    def parse(self, response):
        print("response.url==",response.url)
        print(response.text)

        for node in response.xpath('//div[@class="item"]'):
            # 电影的名称
            name = node.xpath('.//span[@class="title"][1]/text()').extract()[0]
            # 电影的图片
            image = node.xpath('.//div[@class="pic"]/a/img/@src').extract()[0]

            # 电影信息
            info = node.xpath('.//div[@class="bd"]/p[1]/text()').extract()
            if info:
                info = "".join(info)
            # 评分
            star = node.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            # 一句话简介,有一部电影没有，会报错
            desc =  node.xpath('.//span[@class="inq"]/text()').extract()#

            if desc :
                desc = desc[0]


            item =   MoviespiderItem()
            item["name"] = name
            item["image"] = image
            item["info"] = info
            item["star"] = star
            item["desc"] = desc
            print("-------------------------------------------")

            print(item)

            yield item


            #下一页
            if self.offset < 225:
                self.offset += 25

            next_page_url =   self.url+str(self.offset)+"&filter="
            yield scrapy.Request(next_page_url,callback=self.parse)





