"""TypesenseHelper
Wrapper on top of the Typesense API client"""

import typesense
from typesense import exceptions
import json
from builtins import range


class TypesenseHelper:
    """TypesenseHelper"""

    def __init__(self, alias_name, collection_name_tmp):
        self.typesense_client = typesense.Client({
            'api_key': 'xyz',
            'nodes': [{
                'host': 'localhost',
                'port': '8108',
                'protocol': 'http'
            }]
        })
        self.alias_name = alias_name
        self.collection_name_tmp = collection_name_tmp

    def create_tmp_collection(self):
        """Create a temporary index to add records to"""
        try:
            self.typesense_client.collections[self.collection_name_tmp].delete()
        except exceptions.ObjectNotFound:
            pass

        self.typesense_client.collections.create({
            'name': self.collection_name_tmp,
            'fields': [
                {'name': 'anchor', 'type': 'string', 'optional': True},
                {'name': 'content', 'type': 'string', 'optional': True},
                {'name': 'url', 'type': 'string', 'facet': True},
                {'name': 'version', 'type': 'string', 'facet': True},
                {'name': 'item_priority', 'type': 'int64'},
            ],
            'default_sorting_field': 'item_priority'
        })

    def add_records(self, records, url, from_sitemap):
        """Add new records to the temporary index"""
        transformed_records = list(map(TypesenseHelper.transform_record, records))
        record_count = len(transformed_records)

        for i in range(0, record_count, 50):
            result = self.typesense_client.collections[self.collection_name_tmp].documents.import_(
                transformed_records[i:i + 50])
            failed_items = list(
                map(lambda r: json.loads(json.loads(r)),
                    filter(lambda r: json.loads(json.loads(r))['success'] is False, result)))
            if len(failed_items) > 0:
                print(failed_items)
                raise Exception

        color = "96" if from_sitemap else "94"

        print(
            '\033[{}m> DocSearch: \033[0m{}\033[93m {} records\033[0m)'.format(
                color, url, record_count))

    def commit_tmp_collection(self):
        """Update alias to point to new collection"""
        old_collection_name = None

        try:
            old_collection_name = self.typesense_client.aliases[self.alias_name].retrieve()['collection_name']
        except exceptions.ObjectNotFound:
            pass

        self.typesense_client.aliases.upsert(self.alias_name, {'collection_name': self.collection_name_tmp})

        if old_collection_name:
            self.typesense_client.collections[old_collection_name].delete()

    @staticmethod
    def transform_record(record):
        transformed_record = {k: v for k, v in record.items() if v is not None}
        transformed_record['item_priority'] = transformed_record['weight']['page_rank'] * 1000000000 + \
                                              transformed_record['weight']['level'] * 1000 + \
                                              transformed_record['weight']['position']
        return transformed_record
