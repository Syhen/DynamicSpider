# -*- coding: utf-8 -*-
"""
Created on 2017/04/08 17:42:40

@author: mac
"""

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from dynamic.spiders.DynamicSpider import DynamicSpider
from dynamic.spiders.DynamicJSSpider import DynamicJSSpider

import pymongo


if __name__ == '__main__':
    con = pymongo.MongoClient()
    db = con.spider
    ids = [8]
    rules = db.rules.find({'_id': {'$in': ids}})
    con.close()

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    configure_logging(settings)

    for rule in rules:
        runner.crawl(DynamicSpider, rule=rule)
    # for rule in rules:
    #     runner.crawl(DynamicJSSpider, rule=rule)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
