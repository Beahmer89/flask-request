import unittest

from tests import fixtures

import flask_request


class TestHTTPFetch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_class = flask_request.RequestsSession()

    def test_json_encoding(self):
        body = {'post_data': 'to_send', 'foo': [1,2,3]}
        response = self.test_class.http_fetch('https://httpbin.org/post',
                                              method='POST', data=body)
        deserialized_response = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(deserialized_response['json'], body)

    def test_encoding_not_used(self):
        response = self.test_class.http_fetch('https://httpbin.org/get')
        deserialized_response = response.json()

        self.assertEquals(response.status_code, 200)
        self.assertIsNone(deserialized_response.get('json'))

    def test_unsupported_not_used(self):
        headers = {'Content-Type': 'text/html'}
        with self.assertRaises(ValueError):
            self.test_class.http_fetch('https://httpbin.org/post',
                                       method='POST', data={'foo': 'bar'},
                                       headers=headers)
