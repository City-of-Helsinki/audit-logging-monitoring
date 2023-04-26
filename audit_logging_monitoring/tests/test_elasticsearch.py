from django.test import SimpleTestCase, override_settings
from django.conf import settings
import requests
import json
from audit_logging_monitoring.monitoring import add_entry, get_entries



class TestElasticsearch(SimpleTestCase):

    def test_elasticsearch_added_entry_success(self):
        r = add_entry("2023-04-27T00:47:50Z")
        assert r.status_code == 201

    @override_settings(ELASTICSEARCH_HOST="unknown-host")
    def test_elasticsearch_added_entry_failed(self):
        try:
            r = add_entry("2023-04-27T00:47:50Z")
            assert False
        except Exception as err:
            pass

      
    def test_elasticsearch_get_entries_success(self):
        entries = get_entries("2023-04-27T00:47:50Z", "2023-04-26T00:47:50Z")
        empty = True

        for entry in entries:
            empty = False
            break

        if(empty):
            assert False

        