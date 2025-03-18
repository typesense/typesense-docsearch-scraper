import os
from datetime import datetime, timedelta

import pytest
from typesense import Client, exceptions

from scraper.src.typesense_helper import TypesenseHelper

expected_schema = {
    'default_sorting_field': 'item_priority',
    'enable_nested_fields': False,
    'fields': [
        {
            'facet': False,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'anchor',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': False,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'content',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'url',
            'optional': False,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'url_without_anchor',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'version',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string[]',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl0',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl1',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl2',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl3',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl4',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl5',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'hierarchy.lvl6',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'type',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': '.*_tag',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'language',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string',
        },
        {
            'facet': True,
            'index': True,
            'infix': False,
            'locale': 'en',
            'name': 'tags',
            'optional': True,
            'sort': False,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'string[]',
        },
        {
            'facet': False,
            'index': True,
            'infix': False,
            'locale': '',
            'name': 'item_priority',
            'optional': False,
            'sort': True,
            'stem': False,
            'stem_dictionary': '',
            'store': True,
            'type': 'int64',
        },
    ],
    'name': 'collection',
    'num_documents': 0,
    'symbols_to_index': [],
    'token_separators': ['_', '-'],
}


@pytest.fixture
def typesense_client():
    client = Client(
        {
            'api_key': os.environ.get('TYPESENSE_API_KEY', 'xyz'),
            'nodes': [
                {
                    'host': os.environ.get('TYPESENSE_HOST', 'localhost'),
                    'port': os.environ.get('TYPESENSE_PORT', '8108'),
                    'path': os.environ.get('TYPESENSE_PATH', ''),
                    'protocol': os.environ.get('TYPESENSE_PROTOCOL', 'http'),
                }
            ],
            'connection_timeout_seconds': 30 * 60,
        }
    )
    return client


def test_create_tmp_collection(typesense_client):
    """Test that a temporary collection is created with the expected schema"""
    # Arrange
    original_helper = TypesenseHelper('test_alias', 'collection', {})
    original_helper.create_tmp_collection()

    # Act
    ten_seconds_ago_timestamp, now_timestamp = int(
        (datetime.now() - timedelta(seconds=10)).timestamp()
    ), int(datetime.now().timestamp())

    collection_details = typesense_client.collections['collection'].retrieve()

    # Assert that created_at is within the last 10 seconds
    assert (
        ten_seconds_ago_timestamp <= collection_details['created_at'] <= now_timestamp
    )

    # Assert that the schema is as expected
    collection_details.pop('created_at', None)

    assert collection_details == expected_schema

    # Teardown
    typesense_client.collections['collection'].delete()


def test_create_tmp_collection_already_exists(typesense_client):
    """
    Test that if a collection with the temporary name already exists,
    it is deleted and recreated.
    """
    # Arrange
    typesense_client.collections.create(
        {
            'name': 'collection',
            'fields': [
                {
                    'name': 'url',
                    'type': 'string',
                    'facet': True,
                    'optional': False,
                }
            ],
            'token_separators': ['_', '-'],
        }
    )
    original_helper = TypesenseHelper('test_alias', 'collection', {})
    original_helper.create_tmp_collection()

    # Act
    ten_seconds_ago_timestamp, now_timestamp = int(
        (datetime.now() - timedelta(seconds=10)).timestamp()
    ), int(datetime.now().timestamp())

    collection_details = typesense_client.collections['collection'].retrieve()

    # Assert that created_at is within the last 10 seconds
    assert (
        ten_seconds_ago_timestamp <= collection_details['created_at'] <= now_timestamp
    )

    # Assert that the schema is as expected
    collection_details.pop('created_at', None)

    assert collection_details == expected_schema
    # Teardown
    typesense_client.collections['collection'].delete()


def test_transform_record():
    # Arrange
    record = {
        'weight': {'page_rank': 1, 'level': 2, 'position_descending': 3},
        'hierarchy': {
            'lvl0': 'Home',
            'lvl1': 'Products',
            'lvl2': 'Electronics',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None,
        },
        'hierarchy_radio': {
            'lvl0': None,
            'lvl1': None,
            'lvl2': 'Electronics',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None,
        },
        'version': '1.0,2.0',
        'extra_field': None,
    }

    expected_transformed_record = {
        'weight': {'page_rank': 1, 'level': 2, 'position_descending': 3},
        'item_priority': 1000002003,
        'hierarchy.lvl0': 'Home',
        'hierarchy.lvl1': 'Products',
        'hierarchy.lvl2': 'Electronics',
        'hierarchy_radio.lvl2': 'Electronics',
        'version': ['1.0', '2.0'],
        'hierarchy': {
            'lvl0': 'Home',
            'lvl1': 'Products',
            'lvl2': 'Electronics',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None,
        },
        'hierarchy_radio': {
            'lvl0': None,
            'lvl1': None,
            'lvl2': 'Electronics',
            'lvl3': None,
            'lvl4': None,
            'lvl5': None,
            'lvl6': None,
        },
    }

    # Act
    transformed_record = TypesenseHelper.transform_record(record)

    # Assert
    assert transformed_record == expected_transformed_record


def test_add_records(typesense_client):
    """
    Test that records are added to the temporary collection
    with the expected fields
    """
    # Arrange
    records = [
        {
            'weight': {'page_rank': 1, 'level': 2, 'position_descending': 3},
            'hierarchy': {
                'lvl0': 'Home',
                'lvl1': 'Products',
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': None,
                'lvl1': None,
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0,2.0',
            'anchor': 'See More',
            'content': 'Explore our range of electronics',
            'url': 'http://example.com/products/electronics',
            'url_without_anchor': 'http://example.com/products/electronics',
            'type': 'Product Page',
            'language': 'en',
            'tags': ['electronics', 'new arrivals'],
        },
        {
            'weight': {'page_rank': 2, 'level': 1, 'position_descending': 1},
            'hierarchy': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0',
            'anchor': 'Learn More',
            'content': 'Discover more about our company values',
            'url': 'http://example.com/about',
            'url_without_anchor': 'http://example.com/about',
            'type': 'About Page',
            'language': 'en',
            'tags': ['company', 'values'],
        },
    ]
    url = "http://example.com"
    from_sitemap = True

    helper = TypesenseHelper('test_alias', 'collection', {})
    helper.create_tmp_collection()

    # Call the method under test
    helper.add_records(records, url, from_sitemap)

    expected_records = [
        {
            'anchor': 'Learn More',
            'content': 'Discover more about our company values',
            'hierarchy': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy.lvl0': 'About Us',
            'hierarchy_radio.lvl0': 'About Us',
            'id': '1',
            'item_priority': 2000001001,
            'language': 'en',
            'tags': ['company', 'values'],
            'type': 'About Page',
            'url': 'http://example.com/about',
            'url_without_anchor': 'http://example.com/about',
            'version': ['1.0'],
            'weight': {'level': 1, 'page_rank': 2, 'position_descending': 1},
        },
        {
            'anchor': 'See More',
            'content': 'Explore our range of electronics',
            'hierarchy': {
                'lvl0': 'Home',
                'lvl1': 'Products',
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': None,
                'lvl1': None,
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy.lvl0': 'Home',
            'hierarchy.lvl1': 'Products',
            'hierarchy.lvl2': 'Electronics',
            'hierarchy_radio.lvl2': 'Electronics',
            'id': '0',
            'item_priority': 1000002003,
            'language': 'en',
            'tags': ['electronics', 'new arrivals'],
            'type': 'Product Page',
            'url': 'http://example.com/products/electronics',
            'url_without_anchor': 'http://example.com/products/electronics',
            'version': ['1.0', '2.0'],
            'weight': {'level': 2, 'page_rank': 1, 'position_descending': 3},
        },
    ]
    response = typesense_client.collections['collection'].documents.search(
        {
            'q': '*',
        }
    )['hits']

    actual_records = [document['document'] for document in response]

    # Assert
    assert actual_records == expected_records

    # Teardown
    typesense_client.collections['collection'].delete()


def test_commit_tmp_collection(typesense_client):
    """Test that committing a temporary collection works."""
    # Arrange
    records = [
        {
            'weight': {'page_rank': 1, 'level': 2, 'position_descending': 3},
            'hierarchy': {
                'lvl0': 'Home',
                'lvl1': 'Products',
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': None,
                'lvl1': None,
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0,2.0',
            'anchor': 'See More',
            'content': 'Explore our range of electronics',
            'url': 'http://example.com/products/electronics',
            'url_without_anchor': 'http://example.com/products/electronics',
            'type': 'Product Page',
            'language': 'en',
            'tags': ['electronics', 'new arrivals'],
        },
        {
            'weight': {'page_rank': 2, 'level': 1, 'position_descending': 1},
            'hierarchy': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0',
            'anchor': 'Learn More',
            'content': 'Discover more about our company values',
            'url': 'http://example.com/about',
            'url_without_anchor': 'http://example.com/about',
            'type': 'About Page',
            'language': 'en',
            'tags': ['company', 'values'],
        },
    ]
    url = "http://example.com"
    from_sitemap = True

    helper = TypesenseHelper('test_alias', 'collection', {})
    helper.create_tmp_collection()

    original_synonyms = typesense_client.collections['collection'].synonyms.retrieve()[
        'synonyms'
    ]

    original_overrides = typesense_client.collections[
        'collection'
    ].overrides.retrieve()['overrides']

    helper.add_records(records, url, from_sitemap)
    helper.commit_tmp_collection()

    # Act
    tmp_collection_helper = TypesenseHelper('test_alias', 'collection_tmp', {})
    tmp_collection_helper.create_tmp_collection()
    tmp_collection_helper.add_records(records, url, from_sitemap)
    tmp_collection_helper.commit_tmp_collection()

    new_synonyms = typesense_client.collections['collection_tmp'].synonyms.retrieve()[
        'synonyms'
    ]

    new_overrides = typesense_client.collections['collection_tmp'].overrides.retrieve()[
        'overrides'
    ]

    # Assert
    assert (
        typesense_client.aliases['test_alias'].retrieve()['collection_name']
        == 'collection_tmp'
    )

    assert new_synonyms == original_synonyms == []
    assert new_overrides == original_overrides == []

    assert pytest.raises(
        exceptions.ObjectNotFound,
        typesense_client.collections['collection'].retrieve,
    )

    # Teardown
    typesense_client.collections['collection_tmp'].delete()
    typesense_client.aliases['test_alias'].delete()


def test_commit_tmp_collection_with_curation_rules(typesense_client):
    """Test that curation rules are copied from the temporary collection"""
    # Arrange
    records = [
        {
            'weight': {'page_rank': 1, 'level': 2, 'position_descending': 3},
            'hierarchy': {
                'lvl0': 'Home',
                'lvl1': 'Products',
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': None,
                'lvl1': None,
                'lvl2': 'Electronics',
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0,2.0',
            'anchor': 'See More',
            'content': 'Explore our range of electronics',
            'url': 'http://example.com/products/electronics',
            'url_without_anchor': 'http://example.com/products/electronics',
            'type': 'Product Page',
            'language': 'en',
            'tags': ['electronics', 'new arrivals'],
        },
        {
            'weight': {'page_rank': 2, 'level': 1, 'position_descending': 1},
            'hierarchy': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'hierarchy_radio': {
                'lvl0': 'About Us',
                'lvl1': None,
                'lvl2': None,
                'lvl3': None,
                'lvl4': None,
                'lvl5': None,
                'lvl6': None,
            },
            'version': '1.0',
            'anchor': 'Learn More',
            'content': 'Discover more about our company values',
            'url': 'http://example.com/about',
            'url_without_anchor': 'http://example.com/about',
            'type': 'About Page',
            'language': 'en',
            'tags': ['company', 'values'],
        },
    ]
    url = "http://example.com"
    from_sitemap = True

    helper = TypesenseHelper('test_alias_curation', 'collection', {})
    helper.create_tmp_collection()

    override = {
        "rule": {"query": "some thing", "match": "exact"},
        "includes": [{"id": "422", "position": 1}, {"id": "54", "position": 2}],
        "excludes": [{"id": "287"}],
    }

    synonym = {"synonyms": ["some", "maybe", "set"]}

    typesense_client.collections['collection'].synonyms.upsert('some_synonym', synonym)
    typesense_client.collections['collection'].overrides.upsert(
        'some_override', override
    )

    original_synonyms = typesense_client.collections['collection'].synonyms.retrieve()[
        'synonyms'
    ]

    original_overrides = typesense_client.collections[
        'collection'
    ].overrides.retrieve()['overrides']

    helper.add_records(records, url, from_sitemap)
    helper.commit_tmp_collection()

    # Act
    tmp_collection_helper = TypesenseHelper(
        'test_alias_curation', 'collection_tmp_curation', {}
    )
    tmp_collection_helper.create_tmp_collection()
    tmp_collection_helper.add_records(records, url, from_sitemap)
    tmp_collection_helper.commit_tmp_collection()

    new_synonyms = typesense_client.collections[
        'collection_tmp_curation'
    ].synonyms.retrieve()['synonyms']

    new_overrides = typesense_client.collections[
        'collection_tmp_curation'
    ].overrides.retrieve()['overrides']

    # Assert
    assert (
        typesense_client.aliases['test_alias_curation'].retrieve()['collection_name']
        == 'collection_tmp_curation'
    )

    assert new_synonyms == original_synonyms
    assert new_overrides == original_overrides

    assert pytest.raises(
        exceptions.ObjectNotFound,
        typesense_client.collections['collection'].retrieve,
    )

    # Teardown
    typesense_client.collections['collection_tmp_curation'].delete()
    typesense_client.aliases['test_alias_curation'].delete()
