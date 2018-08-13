# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem
import re


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentSpider'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    def parse(self, response):

        for each in response.xpath('//*[contains(@class,"odd") or contains(@class,"even")]'):
            item = TencentItem()
            name = each.xpath('./td[1]/a/text()').extract_first()
            detailLink = each.xpath('./td[2]/text()').extract_first()
            positionInfo = "https://hr.tencent.com/" + each.xpath('./td[1]/a/@href').extract_first()
            peopleNumber = each.xpath('./td[3]/text()').extract_first()
            workLocation = each.xpath('./td[4]/text()').extract_first()
            publishDate = each.xpath('./td[5]/text()').extract_first()

            item['name'] = name
            item['detailLink'] = detailLink
            item['positionInfo'] = positionInfo
            item['peopleNumber'] = peopleNumber
            item['workLocation'] = workLocation
            item['publishDate'] = publishDate

            yield item

        now_page = int(re.search(r'\d+', response.url).group())
        if now_page < 10:
            url = re.sub(r'\d+', str(now_page+10), response.url)

            yield scrapy.Request(url, callback=self.parse)
