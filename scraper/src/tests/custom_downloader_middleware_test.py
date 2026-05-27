from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException

from ..custom_downloader_middleware import CustomDownloaderMiddleware


def _make_driver(ready_states):
    """Driver whose document.readyState returns the next value on each call."""
    states = iter(ready_states)
    driver = MagicMock()
    driver.execute_script.side_effect = lambda *_: next(states)
    driver.page_source = "<html></html>"
    driver.current_url = "https://example.com/"
    return driver


def _make_request(url="https://example.com/"):
    return SimpleNamespace(url=url, replace=lambda url: _make_request(url))


def test_js_wait_is_honored_when_ready_state_completes_quickly():
    """js_wait must apply even when readyState=complete."""
    CustomDownloaderMiddleware.driver = _make_driver(["complete"])
    middleware = CustomDownloaderMiddleware()
    spider = SimpleNamespace(js_render=True, js_wait=3, remove_get_params=False)

    with patch("scraper.src.custom_downloader_middleware.time.sleep") as sleep:
        middleware.process_request(_make_request(), spider)

    sleep.assert_called_once_with(3)


def test_js_wait_is_honored_on_ready_state_timeout():
    CustomDownloaderMiddleware.driver = _make_driver(["loading"])
    middleware = CustomDownloaderMiddleware()
    spider = SimpleNamespace(js_render=True, js_wait=2, remove_get_params=False)

    with (
        patch("scraper.src.custom_downloader_middleware.time.sleep") as sleep,
        patch("scraper.src.custom_downloader_middleware.WebDriverWait") as wait,
    ):
        wait.return_value.until.side_effect = TimeoutException()
        middleware.process_request(_make_request(), spider)

    sleep.assert_called_once_with(2)


def test_zero_js_wait_skips_sleep():
    CustomDownloaderMiddleware.driver = _make_driver(["complete"])
    middleware = CustomDownloaderMiddleware()
    spider = SimpleNamespace(js_render=True, js_wait=0, remove_get_params=False)

    with patch("scraper.src.custom_downloader_middleware.time.sleep") as sleep:
        middleware.process_request(_make_request(), spider)

    sleep.assert_not_called()


def test_js_render_disabled_short_circuits():
    CustomDownloaderMiddleware.driver = MagicMock()
    middleware = CustomDownloaderMiddleware()
    spider = SimpleNamespace(js_render=False, js_wait=5, remove_get_params=False)

    assert middleware.process_request(_make_request(), spider) is None
    middleware.driver.get.assert_not_called()
