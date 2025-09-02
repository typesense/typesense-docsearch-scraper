# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config
import pytest


class TestFlushIntervalSeconds:
    @staticmethod
    def test_default_flush_interval_seconds():
        """Should use default flush_interval_seconds of 60 when not specified"""
        c = config({})

        config_loaded = ConfigLoader(c)

        assert config_loaded.flush_interval_seconds == 60

    def test_custom_flush_interval_seconds(self):
        """Should use custom flush_interval_seconds when specified in config"""
        c = config({"flush_interval_seconds": 30})

        config_loaded = ConfigLoader(c)

        assert config_loaded.flush_interval_seconds == 30

    def test_flush_interval_seconds_zero(self):
        """Should raise exception when flush_interval_seconds is 0"""
        c = config({"flush_interval_seconds": 0})

        with pytest.raises(Exception, match="flush_interval_seconds should be a positive integer"):
            ConfigLoader(c)

    def test_flush_interval_seconds_negative(self):
        """Should raise exception when flush_interval_seconds is negative"""
        c = config({"flush_interval_seconds": -30})

        with pytest.raises(Exception, match="flush_interval_seconds should be a positive integer"):
            ConfigLoader(c)

    def test_flush_interval_seconds_string(self):
        """Should raise exception when flush_interval_seconds is a string"""
        c = config({"flush_interval_seconds": "30"})

        with pytest.raises(Exception, match="flush_interval_seconds should be an integer"):
            ConfigLoader(c)

    def test_flush_interval_seconds_float(self):
        """Should raise exception when flush_interval_seconds is a float"""
        c = config({"flush_interval_seconds": 30.5})

        with pytest.raises(Exception, match="flush_interval_seconds should be an integer"):
            ConfigLoader(c)

    def test_flush_interval_seconds_large_value(self):
        """Should accept large flush_interval_seconds values"""

        c = config({"flush_interval_seconds": 3600})

        config_loaded = ConfigLoader(c)

        assert config_loaded.flush_interval_seconds == 3600

    def test_flush_interval_seconds_one(self):
        """Should accept flush_interval_seconds of 1"""

        c = config({"flush_interval_seconds": 1})

        config_loaded = ConfigLoader(c)

        assert config_loaded.flush_interval_seconds == 1
