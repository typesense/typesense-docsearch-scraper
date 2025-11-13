"""TypesenseHelper
Wrapper on top of the Typesense API client"""

import json
import os
from builtins import range

import typesense
from typesense import exceptions


class TypesenseHelper:
    """TypesenseHelper"""

    def __init__(self, alias_name, collection_name_tmp, custom_settings):
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
        version = self.typesense_client.debug.retrieve().get("version")
        if version == "nightly":
            self.typesense_version = 30
        else:
            self.typesense_version = int(version.split(".")[0])

    def create_tmp_collection(self):
        """Create a temporary index to add records to"""
        try:
            self.typesense_client.collections[self.collection_name_tmp].delete()
        except exceptions.ObjectNotFound:
            pass

        general_schema = {
            "name": self.collection_name_tmp,
            "fields": [
                {"name": "anchor", "type": "string", "optional": True},
                {
                    "name": "content",
                    "type": "string",
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {"name": "url", "type": "string", "facet": True},
                {
                    "name": "url_without_anchor",
                    "type": "string",
                    "facet": True,
                    "optional": True,
                },
                {
                    "name": "version",
                    "type": "string[]",
                    "facet": True,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl0",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl1",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl2",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl3",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl4",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl5",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "hierarchy.lvl6",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": "type",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {
                    "name": ".*_tag",
                    "type": "string",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {"name": "language", "type": "string", "facet": True, "optional": True},
                {
                    "name": "tags",
                    "type": "string[]",
                    "facet": True,
                    "locale": self.collection_locale,
                    "optional": True,
                },
                {"name": "item_priority", "type": "int64"},
            ],
            "default_sorting_field": "item_priority",
            "token_separators": ["_", "-"],
        }

        if self.typesense_version >= 30:
            try:
                old_collection = self.typesense_client.collections[
                    self.collection_name_tmp
                ].retrieve()
                curation_sets = old_collection.get("curation_sets", [])

                synonym_sets = old_collection.get("synonym_sets", [])
            except exceptions.ObjectNotFound:
                curation_sets = []
                synonym_sets = []

            schema = {
                **general_schema,
                "curation_sets": curation_sets,
                "synonym_sets": synonym_sets,
            }
        else:
            schema = general_schema

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
        """Add new records to the temporary index"""
        transformed_records = list(map(TypesenseHelper.transform_record, records))
        record_count = len(transformed_records)

        for i in range(0, record_count, 50):
            result = self.typesense_client.collections[
                self.collection_name_tmp
            ].documents.import_(transformed_records[i : i + 50])

            # Check for failed items directly without double-decoding
            failed_items = [
                r for r in result if r.get('success') is False
            ]
            if len(failed_items) > 0:
                print(failed_items)
                raise Exception

        color = "96" if from_sitemap else "94"

        print(
            '\033[{}m> DocSearch: \033[0m{}\033[93m {} records\033[0m)'.format(
                color, url, record_count
            )
        )

    def commit_tmp_collection(self):
        """Update alias to point to new collection"""
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
        if self.typesense_version >= 30:
            return

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
        if self.typesense_version >= 30:
            return

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
