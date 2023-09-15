BOT_NAME = "tore"
SPIDER_MODULES = ["tore.spiders"]
NEWSPIDER_MODULE = "tore.spiders"
SPLASH_URL = "http://0.0.0.0:8050"  # "http://192.168.59.103:8050"
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"
PROXY_POOL_ENABLED = True
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
)
ROBOTSTXT_OBEY = False
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
}

DOWNLOADER_MIDDLEWARES = {
    # "scrapy_proxy_pool.middlewares.ProxyPoolMiddleware": 610,
    # "scrapy_proxy_pool.middlewares.BanDetectionMiddleware": 620,
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # "scrapy.pipelines.files.FilesPipeline": 1
    "tore.pipelines.ToreItemExtractor": 100,
    # "tore.pipelines.ToreFilesPipeline": 100,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
