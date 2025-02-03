import os
import pdb
from unittest.mock import MagicMock

import pytest
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError


@pytest.fixture
def config():
    return MagicMock(
        index_name="test_index",
        start_urls=[{"url": "http://example.com"}],
        allowed_domains=["example.com"],
        stop_urls=[],
        js_render=False,
    )


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv("DOCSEARCH_BASICAUTH_USERNAME", "testuser")
    monkeypatch.setenv("DOCSEARCH_BASICAUTH_PASSWORD", "testpass")
    monkeypatch.setenv("DOCSEARCH_AUTH_DOMAIN", "http://example.com")


def test_spider_auth_attributes(config, env_vars):
    """Test that DocumentationSpider correctly sets up Basic Auth attributes"""
    from scraper.src.documentation_spider import DocumentationSpider

    spider = DocumentationSpider(config=config, typesense_helper=None, strategy=None)

    assert spider.http_user == "testuser"
    assert spider.http_pass == "testpass"
    assert spider.http_auth_domain == "http://example.com"
