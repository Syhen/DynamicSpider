# -*- coding: utf-8 -*-

# Scrapy settings for dynamic project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'dynamic'

SPIDER_MODULES = ['dynamic.spiders']
NEWSPIDER_MODULE = 'dynamic.spiders'

# MONGO CONFIGS
MONGO_URL = 'mongodb://localhost:27017'
MONGO_DB = 'spider'
MONGO_INFO_COLLECTION = 'info'
MONGO_HISTORY_COLLECTION = 'history_info'

# LOG LEVEL
LOG_LEVEL = 'INFO'  # ERROR, INFO, WARNING, DEBUG

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'dynamic (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}

ITEM_PIPELINES = {
    'dynamic.pipelines.DynamicPipeline': 300,
    'dynamic.pipelines.DynamicHistoryPipeline': 800,
}

SPLASH_URL = 'http://127.0.0.1:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
