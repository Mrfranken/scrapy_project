# -*- coding: utf-8 -*-

# Scrapy settings for bole_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'bole_scrapy'

SPIDER_MODULES = ['bole_scrapy.spiders']
NEWSPIDER_MODULE = 'bole_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'bole_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'bole_scrapy.middlewares.BoleScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'bole_scrapy.middlewares.BoleScrapyDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'bole_scrapy.pipelines.BoleScrapyPipeline': 300,
    # 'scrapy.pipelines.images.ImagesPipeline': 30, # 处理图片的pipelines, 数字越小越早进入pipeline进行处理
    #  'bole_scrapy.pipelines.JsonExporterPipeline': 2,
    # 'bole_scrapy.pipelines.MysqlTwistedPipline': 4,
    'bole_scrapy.pipelines.MysqlPipeline': 3,
    # 'bole_scrapy.pipelines.JsonWithEncodingPipeline': 2,
    # 'bole_scrapy.pipelines.ArticleImagesPipeline': 1,
}

# 下载图片的配置 pipelines/images.py中self.images_urls_field将从settings文件中读取这个值然后给get_media_requests进行处理
IMAGES_URLS_FIELD = "article_image_url"
IMAGES_MIN_WIDTH = 100
IMAGES_MIN_HEIGHT = 100  # 下载的图片必须大于100 * 100

# 跟IMAGES_URLS_FIELD一样这个字段也是定义在 pipelines/images.py 中的
IMAGES_STORE = os.path.join(os.path.dirname(__file__), "images")  # 图片的保存路径配置

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'ariticle_spider'
MYSQL_TABLENAME = 'jobbole_article'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '8823443wsj_WIN'


if __name__ == '__main__':
    print(IMAGES_STORE)
