import logging

from scrapy import signals


class HeaderInspectionMiddleware:
    """
    Middleware to inspect headers of outgoing requests and incoming responses
    """

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
        logging.debug(f"\nOutgoing request to: {request.url}")
        logging.debug(f"\nHeaders: {request.headers}")
