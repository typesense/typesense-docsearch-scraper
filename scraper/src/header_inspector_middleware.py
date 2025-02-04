import logging

from scrapy import signals


class HeaderInspectionMiddleware:
    """
    Middleware to inspect headers of outgoing requests and incoming responses
    """

    def __init__(self):
        self.spider = None

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        self.spider = spider

    def process_request(self, request, spider):
        """
        This method is called for each request that goes through the download middleware.
        """
        logging.debug("\nOutgoing request to: %s", request.url)
        logging.debug("\nHeaders: %s", request.headers)
