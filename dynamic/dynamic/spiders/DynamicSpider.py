# -*- coding: utf-8 -*-
"""
Created on 2017/04/08 17:38:48

@author: mac
"""

import scrapy
from dynamic.items import ItemMaker


class DynamicSpider(scrapy.Spider):
    """dynamic spider class."""
    name = 'dynamic_spider'

    def __init__(self, rule=None, *args, **kwargs):
        super(DynamicSpider, self).__init__(*args, **kwargs)
        self.DynamicItem = ItemMaker(rule['item_name'])
        self.rule = rule

    def start_requests(self):
        for url in self.rule['start_url']:
            yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        print response.url
        body_list = response.xpath(self.rule['body_list'])
        for body in body_list:
            item = self.DynamicItem()
            meta = self.rule['meta']
            item.update(meta)
            for name in self.rule['xpath']:
                item['_'.join(name.split('_')[:-1])] = body.xpath(self.rule['xpath'][name]).extract()[0]
            print item
        next_page = response.xpath(self.rule['next_page'])
        if next_page:
            yield scrapy.Request(
                next_page.extract()[0],
                callback=self.parse,
                dont_filter=True
            )
