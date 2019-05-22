# -*- coding: utf-8 -*-
import scrapy
from changde.items import ChangdeItem


class HtggSpider(scrapy.Spider):
    name = 'htgg'
    allowed_domains = ['ccgp-hunan.gov.cn']
    # start_urls = ['http://ccgp-hunan.gov.cn/']
    # 合同公告板块

    def start_requests(self):
        start_url = 'http://changd.ccgp-hunan.gov.cn/f/m/notice_prod/c_2'
        yield scrapy.FormRequest(
            url=start_url,
            formdata={"page": "0", "areaNo": "430700", "typeNo": "7"}
        )
    #     post请求

    def parse(self, response):
        items = ChangdeItem()
        titleList = response.xpath('//div[@class="list-group"]/a')
        for item in titleList:
            items['url'] = item.xpath('@href').extract()[0]
            items['public_time'] = item.xpath('./h5/small/span').extract()[0]
            items['title'] = item.xpath('./h5/text()').extract()[0].strip()
            yield items
