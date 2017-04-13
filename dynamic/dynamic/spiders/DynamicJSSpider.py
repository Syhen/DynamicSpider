# -*- coding: utf-8 -*-
"""
Created on 2017/04/12 23:33:53

@author: mac
"""

from dynamic.spiders.DynamicSpider import DynamicSpider
from scrapy_splash import SplashRequest


class DynamicJSSpider(DynamicSpider):
    """dynamic spider class.
    this spider class support javascript. but it is base on the url.
    that means you can not use this to download page modified by javascript which url has not been changed.
    the spider will wait for a page while it is still loading.
    you should just provide a next_page selector by jquery.
    """
    name = 'dynamic_js_spider'

    def __init__(self, rule=None, *args, **kwargs):
        super(DynamicJSSpider, self).__init__(rule, *args, **kwargs)
        # add splash script, use rule['next_page'] to go to the next page.
        self.wait_for_complete = """
        function main(splash)
            assert(splash:go(splash.args.url))
            while not splash:evaljs("document.readyState === 'complete'") do
                splash:wait(0.05)
            end
            return {html=splash:html(), url=splash:url()}
        end
        """
        self.go_next_page = """
        function main(splash)
            splash:go(splash.args.url)
            -- waiting splash.args.url loaded.
            while not splash:evaljs("document.readyState === 'complete'") do
                splash:wait(0.05)
            end
            -- begin click while splash.args.url complete.
            splash:runjs("$('%s').click()")
            -- click will not change readyState immediately.
            -- while the page start loading, break the loop.
            local start_loading = false
            while not start_loading do
              splash:wait(0.01)
              start_loading = splash:evaljs("document.readyState != 'complete'")
            end
            -- loading new pages, wait for complete.
            local status = splash:evaljs("document.readyState === 'complete'")
            while not status do
                splash:wait(0.05)
                status = splash:evaljs("document.readyState === 'complete'")
            end
            return {html=splash:html(), url=splash:url()}
        end
        """ % (self.rule['next_selector'])

    def start_requests(self):
        """you can add more start_url to speed up.
        the best split for urls is equal division.
        """
        for url in self.rule['start_url']:
            yield SplashRequest(
                url,
                self.parse,
                endpoint='execute',
                args={
                    'url': url.encode('ascii'),
                    'lua_source': self.wait_for_complete
                }
            )

    def parse(self, response):
        self.logger.info(response.url)
        for item in self.parse_step(response):
            yield item

        next_page = response.xpath(self.rule['next_page'])
        if next_page and self.pages <= self.rule['max_page']:
            yield SplashRequest(
                response.data['url'],
                callback=self.parse,
                endpoint='execute',
                args={
                    'url': response.url.encode('ascii'),  # avoid SplashRequest's unicode error.
                    'lua_source': self.go_next_page,
                }
            )

