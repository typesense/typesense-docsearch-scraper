"""
CustomDownloaderMiddleware
"""

import time
from urllib.parse import unquote_plus, urlparse

from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


class CustomDownloaderMiddleware:
    driver = None

    def __init__(self):
        self.driver = CustomDownloaderMiddleware.driver

    def process_request(self, request, spider):
        if not spider.js_render:
            return None

        if spider.remove_get_params:
            o = urlparse(request.url)
            url_without_params = o.scheme + "://" + o.netloc + o.path
            request = request.replace(url=url_without_params)

        print("Getting " + request.url + " from selenium")

        self.driver.get(unquote_plus(
            request.url))  # Decode url otherwise firefox is not happy. Ex /#%21/ => /#!/%21

        try:
            # Wait for DOM ready
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            time.sleep(spider.js_wait)

        body = self.driver.page_source.encode("utf-8")
        return HtmlResponse(url=self.driver.current_url, body=body, encoding="utf8")

    def process_response(self, request, response, spider):
        # Since scrappy use start_urls and stop_urls before creating the request
        # If the url get redirected then this url gets crawled even if it's not allowed to
        # So we check if the final url is allowed

        if spider.remove_get_params:
            o = urlparse(response.url)
            url_without_params = o.scheme + "://" + o.netloc + o.path
            response = response.replace(url=url_without_params)

        if response.url == request.url + "#":
            response = response.replace(url=request.url)

        return response
