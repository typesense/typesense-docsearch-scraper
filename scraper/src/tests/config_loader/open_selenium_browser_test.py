# coding: utf-8
from ...config.config_loader import ConfigLoader
from ...config.browser_handler import BrowserHandler
from .abstract import config


class TestOpenSeleniumBrowser:
    def test_browser_not_needed_by_default(self):
        c = config()

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is False

    def test_browser_needed_when_js_render_true(self, monkeypatch):
        from .mocked_init import MockedInit
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())
        monkeypatch.setattr("time.sleep", lambda x: "")
        # When
        c = config({
            "js_render": True
        })

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is True

    def test_browser_needed_when_config_contains_automatic_tag(self,
                                                               monkeypatch):
        from .mocked_init import MockedInit
        monkeypatch.setattr("selenium.webdriver.chrome",
                            lambda x: MockedInit())
        monkeypatch.setattr("time.sleep", lambda x: "")

        # When
        c = config({
            "start_urls": [
                {
                    "url": "https://example.com/(?P<var1>.*?)/(?P<var2>.*?)/",
                    "variables": {
                        "var1": {
                            "url": "https://example.com",
                            "js": "return JSON.stringify(\
                document.getElementsByTagName('h1')[0].textContent.split(' '))"
                        },
                        "var2": ["one", "two", "three"]
                    }
                }
            ]
        })

        actual = ConfigLoader(c)

        assert BrowserHandler.conf_need_browser(actual.config_original_content,
                                                actual.js_render) is True
