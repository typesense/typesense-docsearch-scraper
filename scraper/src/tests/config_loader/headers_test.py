# coding: utf-8
from ...config.config_loader import ConfigLoader
from .abstract import config
import pytest


class TestInit:
    def test_header(self):
        """ Should have a header """
        # Given
        c = config({
            'headers': {
                'Authorization': 'Bearer xyz'
            }
        })

        config_loaded = ConfigLoader(c)

        assert config_loaded.headers == {
                'Authorization': 'Bearer xyz'
        }

    def test_multiple_header(self):
        """ Should have headers """
        # Given
        c = config({
            'headers': {
                'Authorization': 'Bearer xyz',
                'Custom': 1,
            }
        })

        config_loaded = ConfigLoader(c)

        assert config_loaded.headers == {
                'Authorization': 'Bearer xyz',
                'Custom': 1,
        }
