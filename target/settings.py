# -*- coding: utf-8 -*-

# Scrapy settings for target project
#
BOT_NAME = 'target'

SPIDER_MODULES = ['target.spiders']
NEWSPIDER_MODULE = 'target.spiders'

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.39',
]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'target.middlewares.UserAgentDownloaderMiddleware': 400,
    'target.middlewares.ProxyDownloaderMiddleware': 410,
    'target.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = {
    'target.pipelines.TargetPipeline': 300,
}