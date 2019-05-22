# -*- coding: utf-8 -*-
import scrapy
import re
from changde.items import ChangdeItem


class CaigouSpider(scrapy.Spider):
    name = 'caigou'
    allowed_domains = ['ccgp-hunan.gov.cn']
    # start_urls = ['http://ccgp-hunan.gov.cn/']

    def start_requests(self):
        start_url = 'http://changd.ccgp-hunan.gov.cn/f/m/notice_prod/c_2-page_0'
        yield scrapy.Request(
            url=start_url,
        )

    def parse(self, response):
        # items = ChangdeItem()
        titleList = response.xpath('//div[@class="list-group"]/a')
        for item in titleList:
            # items['url'] = item.xpath('@href').extract()[0]
            # items['public_time'] = item.xpath('./h5/small/span')[0].xpath('./text()').extract()[0]
            # items['title'] = item.xpath('./h5/text()').extract()[0].strip()
            url = item.xpath('@href').extract()[0]
            public_time = item.xpath('./h5/small/span')[0].xpath('./text()').extract()[0]
            title = item.xpath('./h5/text()').extract()[0].strip()
            noticeId = re.search(r'c_2-n_(\d+)', url, re.M|re.I).group(0)
            # yield items
            yield scrapy.Request('http://changd.ccgp-hunan.gov.cn/f/m/notice/{}'.format(noticeId), callback=self.parse_item, meta={'url': url, 'public_time': public_time, 'title': title})
    #         通过meta向下一个parse方法传递字典

    def parse_item(self, response):
        items = ChangdeItem()
        # 通过response.meta获取字典中的键值对
        items['content'] = response.text
        items['url'] = response.meta['url']
        items['public_time'] = response.meta['public_time']
        items['title'] = response.meta['title']
        # 在最后一个parse方法中一次性将item返回(piplines中的parse_item会进行接收并处理)
        yield items
