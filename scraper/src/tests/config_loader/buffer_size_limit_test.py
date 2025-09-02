# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config
import pytest


class TestBufferSizeLimit:
    @staticmethod
    def test_default_buffer_size_limit():
        """Should use default buffer_size_limit of 1000 when not specified"""
        c = config({})

        config_loaded = ConfigLoader(c)

        assert config_loaded.buffer_size_limit == 1000

    def test_custom_buffer_size_limit(self):
        """Should use custom buffer_size_limit when specified in config"""
        c = config({"buffer_size_limit": 500})

        config_loaded = ConfigLoader(c)

        assert config_loaded.buffer_size_limit == 500

    def test_buffer_size_limit_zero(self):
        """Should raise exception when buffer_size_limit is 0"""
        c = config({"buffer_size_limit": 0})

        with pytest.raises(Exception, match="buffer_size_limit should be a positive integer"):
            ConfigLoader(c)

    def test_buffer_size_limit_negative(self):
        """Should raise exception when buffer_size_limit is negative"""
        c = config({"buffer_size_limit": -100})

        with pytest.raises(Exception, match="buffer_size_limit should be a positive integer"):
            ConfigLoader(c)

    def test_buffer_size_limit_string(self):
        """Should raise exception when buffer_size_limit is a string"""
        c = config({"buffer_size_limit": "500"})

        with pytest.raises(Exception, match="buffer_size_limit should be an integer"):
            ConfigLoader(c)

    def test_buffer_size_limit_float(self):
        """Should raise exception when buffer_size_limit is a float"""
        c = config({"buffer_size_limit": 500.5})

        with pytest.raises(Exception, match="buffer_size_limit should be an integer"):
            ConfigLoader(c)

    def test_buffer_size_limit_large_value(self):
        """Should accept large buffer_size_limit values"""

        c = config({"buffer_size_limit": 10000})

        config_loaded = ConfigLoader(c)

        assert config_loaded.buffer_size_limit == 10000

    def test_buffer_size_limit_one(self):
        """Should accept buffer_size_limit of 1"""

        c = config({"buffer_size_limit": 1})

        config_loaded = ConfigLoader(c)

        assert config_loaded.buffer_size_limit == 1
