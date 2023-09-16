from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import tore.spiders as spiders


class App:
    def __init__(self):
        self.runner = CrawlerRunner()
        settings = get_project_settings()
        configure_logging(settings)

    @defer.inlineCallbacks
    def run(self):
        # Add all of the spiders that you want to launch to the runner.
        yield self.runner.crawl(spiders.EpisodeScraper)
        yield self.runner.crawl(spiders.DocumentaryScraper)
        yield self.runner.crawl(spiders.StereoScraper)
        yield self.runner.crawl(spiders.EpisodeScraper)
        reactor.stop()


if __name__ == "__main__":
    app = App()
    app.run()
    reactor.run()
