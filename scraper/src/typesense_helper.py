"""TypesenseHelper
Wrapper on top of the Typesense API client"""

import json
import os
from builtins import range
import time

import typesense
from typesense import exceptions


class TypesenseHelper:
    """TypesenseHelper"""

    def __init__(self, alias_name, collection_name_tmp, custom_settings, buffer_size_limit, flush_interval_seconds):
        self.typesense_client = typesense.Client(
            {
                'api_key': os.environ.get('TYPESENSE_API_KEY', None),
                'nodes': [
                    {
                        'host': os.environ.get('TYPESENSE_HOST', None),
                        'port': os.environ.get('TYPESENSE_PORT', None),
                        'path': os.environ.get('TYPESENSE_PATH', ''),
                        'protocol': os.environ.get('TYPESENSE_PROTOCOL', None),
                    }
                ],
                'connection_timeout_seconds': int(os.environ.get('TYPESENSE_CONNECTION_TIMEOUT_SECONDS', 30 * 60)),
                'retry_interval_seconds': int(os.environ.get('TYPESENSE_RETRY_INTERVAL_SECONDS', 1)),
                'num_retries': int(os.environ.get('TYPESENSE_NUM_RETRIES', 3)),
                'healthcheck_interval_seconds': int(os.environ.get('TYPESENSE_HEALTHCHECK_INTERVAL_SECONDS', 60)),
                'verify': os.environ.get('TYPESENSE_VERIFY', 'True').lower() == 'true',
            }
        )
        self.alias_name = alias_name
        self.collection_name_tmp = collection_name_tmp
        self.collection_locale = os.environ.get('TYPESENSE_COLLECTION_LOCALE', 'en')
        self.custom_settings = custom_settings
        self.buffer_size_limit = buffer_size_limit
        self.flush_interval_seconds = flush_interval_seconds

        print(f'\033[93m> DocSearch: Batching config - buffer_size_limit: {self.buffer_size_limit}, flush_interval_seconds: {self.flush_interval_seconds}\033[0m')

        # buffer for batching records
        self.records_buffer = []
        self.buffer_stats = {"total_records": 0, "urls_processed": 0}
        self.last_flush_time = time.time()

    def create_tmp_collection(self):
        """Create a temporary index to add records to"""
        try:
            self.typesense_client.collections[self.collection_name_tmp].delete()
        except exceptions.ObjectNotFound:
            pass

        schema = {
            'name': self.collection_name_tmp,
            'fields': [
                {'name': 'anchor', 'type': 'string', 'optional': True},
                {
                    'name': 'content',
                    'type': 'string',
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {'name': 'url', 'type': 'string', 'facet': True},
                {
                    'name': 'url_without_anchor',
                    'type': 'string',
                    'facet': True,
                    'optional': True,
                },
                {
                    'name': 'version',
                    'type': 'string[]',
                    'facet': True,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl0',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl1',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl2',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl3',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl4',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl5',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'hierarchy.lvl6',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': 'type',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {
                    'name': '.*_tag',
                    'type': 'string',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {'name': 'language', 'type': 'string', 'facet': True, 'optional': True},
                {
                    'name': 'tags',
                    'type': 'string[]',
                    'facet': True,
                    'locale': self.collection_locale,
                    'optional': True,
                },
                {'name': 'item_priority', 'type': 'int64'},
            ],
            'default_sorting_field': 'item_priority',
            'token_separators': ['_', '-'],
        }

        if self.custom_settings is not None:
            token_separators = self.custom_settings.get('token_separators', None)
            if token_separators is not None:
                schema['token_separators'] = token_separators

            symbols_to_index = self.custom_settings.get('symbols_to_index', None)
            if symbols_to_index is not None:
                schema['symbols_to_index'] = symbols_to_index

            field_definitions = self.custom_settings.get('field_definitions', None)
            if field_definitions is not None:
                schema['fields'] = field_definitions

            enable_nested_fields = self.custom_settings.get('enable_nested_fields', None)
            if enable_nested_fields is not None:
                schema['enable_nested_fields'] = enable_nested_fields

        self.typesense_client.collections.create(schema)

    def add_records(self, records, url, from_sitemap):
        """Add new records to the buffer and flush based on size/time thresholds"""
        transformed_records = list(map(TypesenseHelper.transform_record, records))
        record_count = len(transformed_records)

        # Add to buffer
        self.records_buffer.extend(transformed_records)
        self.buffer_stats["total_records"] += record_count
        self.buffer_stats["urls_processed"] += 1

        current_time = time.time()

        flush = {
            'should_flush': False,
            'reason': ''
        }


        # Check size-based flush
        if len(self.records_buffer) >= self.buffer_size_limit:
            flush['should_flush'] = True
            flush['reason'] = f"buffer size ({len(self.records_buffer)} >= {self.buffer_size_limit})"

        # Check time-based flush
        elif current_time - self.last_flush_time >= self.flush_interval_seconds and self.records_buffer:
            flush['should_flush'] = True
            flush['reason'] = f"time interval ({self.flush_interval_seconds}s)"

        if flush['should_flush']:
            self._flush_buffer(flush.get('reason', "unknown reason"))

        color = "96" if from_sitemap else "94"
        print(
            "\033[{}m> DocSearch: \033[0m{}\033[93m {} records (buffered: {})\033[0m".format(
                color, url, record_count, len(self.records_buffer)
            )
        )

    def _flush_buffer(self, reason):
        """Send buffered records to Typesense"""
        if not self.records_buffer:
            return

        print(
            f'\033[94m> DocSearch: Flushing {len(self.records_buffer)} records from {self.buffer_stats["urls_processed"]} URLs (Reason: {reason})\033[0m'
        )

        result = self.typesense_client.collections[
            self.collection_name_tmp
        ].documents.import_(self.records_buffer)

        failed_items = [r for r in result if r.get("success") is False]
        if len(failed_items) > 0:
            print(failed_items)
            raise Exception

        print(
            f"\033[94m> DocSearch: Successfully imported {len(self.records_buffer)} records\033[0m"
        )

        self.records_buffer = []
        self.last_flush_time = time.time()

    def commit_tmp_collection(self):
        """Update alias to point to new collection"""
        if self.records_buffer:
            self._flush_buffer("commit_tmp_collection")

        old_collection_name = self._get_old_collection_name()

        if old_collection_name:
            self._transfer_synonyms(old_collection_name)
            self._transfer_overrides(old_collection_name)

        self.typesense_client.aliases.upsert(
            self.alias_name, {'collection_name': self.collection_name_tmp}
        )

        if old_collection_name:
            self.typesense_client.collections[old_collection_name].delete()

    @staticmethod
    def transform_record(record):
        transformed_record = {k: v for k, v in record.items() if v is not None}
        transformed_record['item_priority'] = (
            transformed_record['weight']['page_rank'] * 1000000000
            + transformed_record['weight']['level'] * 1000
            + transformed_record['weight']['position_descending']
        )

        # Flatten nested hierarchy fields
        for x in range(0, 7):
            if 'hierarchy' in record and f'lvl{x}' in record['hierarchy']:
                if record['hierarchy'][f'lvl{x}'] is not None:
                    transformed_record[f'hierarchy.lvl{x}'] = record['hierarchy'][f'lvl{x}']
            if 'hierarchy_radio' in record and f'lvl{x}' in record['hierarchy_radio']:
                if record['hierarchy_radio'][f'lvl{x}'] is not None:
                    transformed_record[f'hierarchy_radio.lvl{x}'] = record['hierarchy_radio'][f'lvl{x}']

        # Convert version to array
        if 'version' in record and type(record['version']) == str:
            transformed_record['version'] = record['version'].split(',')

        return transformed_record

    def _get_old_collection_name(self):
        """Get the old collection name from the alias"""
        try:
            return self.typesense_client.aliases[self.alias_name].retrieve()[
                'collection_name'
            ]
        except exceptions.ObjectNotFound:
            return None

    def _transfer_synonyms(self, old_collection_name):
        """Transfer synonyms from old collection to new collection"""
        synonyms = (
            self.typesense_client.collections[old_collection_name]
            .synonyms.retrieve()
            .get('synonyms', [])
        )
        for synonym in synonyms:
            synonym_keys = {key: synonym[key] for key in synonym if key != 'id'}
            self.typesense_client.collections[self.collection_name_tmp].synonyms.upsert(
                synonym['id'], synonym_keys
            )

    def _transfer_overrides(self, old_collection_name):
        """Transfer overrides from old collection to new collection"""
        overrides = (
            self.typesense_client.collections[old_collection_name]
            .overrides.retrieve()
            .get('overrides', [])
        )
        for override in overrides:
            override_keys = {key: override[key] for key in override if key != 'id'}
            self.typesense_client.collections[
                self.collection_name_tmp
            ].overrides.upsert(override['id'], override_keys)
