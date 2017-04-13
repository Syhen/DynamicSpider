# -*- coding: utf-8 -*-
"""
Created on 2017/04/08 17:38:48

@author: mac
"""

import re
import scrapy
from dynamic.items import ItemMaker


class DynamicSpider(scrapy.Spider):
    """dynamic spider class."""
    name = 'dynamic_spider'

    def __init__(self, rule=None, *args, **kwargs):
        super(DynamicSpider, self).__init__(*args, **kwargs)
        self.DynamicItem = ItemMaker(rule['item_name'])
        self.rule = rule
        self.pages = 1

    def start_requests(self):
        for url in self.rule['start_url']:
            yield scrapy.Request(
                url,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        for item in self.parse_step(response):
            yield item

        # next page
        next_page = response.xpath(self.rule['next_page'])
        if next_page and self.pages <= self.rule['max_page']:
            yield scrapy.Request(
                next_page.extract()[0],
                callback=self.parse,
                dont_filter=True
            )

    def parse_step(self, response):
        """
        all spider parse will go through the way as:
        1.crawl data from page;(use xpath or css)
        2.get info from crawled messages;(use regulation)
        3.join messages;(str + str)
        :param response: response object.
        :return: yield item or Request object.
        """
        self.pages += 1
        body_list = response.xpath(self.rule['body_list'])
        for body in body_list:
            item = self.DynamicItem()
            meta = self.rule['meta']
            item.update(meta)
            # xpath extract
            for name in self.rule['xpath']:
                item['_'.join(name.split('_')[:-1])] = self.extract(body, name, self.rule, response)

            # get message extract
            for key in self.rule['re']:
                reg = self.rule['re'][key]['reg']
                string = item[self.rule['re'][key]['str_name']]
                reg = re.compile(str('%s' % reg))  # translate u'' -> r''
                result = reg.search(string)
                item[key] = result and result.group(0) or ''

            # join
            for key in self.rule['join']:
                join_dict = self.rule['join'][key]
                item[key] = join_dict['prefix'] + join_dict['join_str'] + item[join_dict['end_name']]
            yield item

    @staticmethod
    def extract(parent_element, name, rule, response):
        """
        extract by deffrent roles of selector.
        :param parent_element: parent element
        :param name: item name
        :param rule: spider's rule. In this class, use `self.rule`
        :param response: scrapy response object
        :return: item value
        """
        item_value = ''.join(parent_element.xpath(rule['xpath'][name]['selector']).extract())
        result = dict(
            normal=item_value,
            url=response.urljoin(item_value)
        )
        return result[rule['xpath'][name]['role']]
