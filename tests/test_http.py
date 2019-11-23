from flask import Flask
import unittest

from tests import fixtures

import flask_request


class TestHTTPFetch(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.app_name = 'fancy_app'
        cls.app = Flask(cls.app_name)
        cls.test_class = flask_request.RequestsSession(cls.app)

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

    def test_user_agent_header_uses_application_not_version(self):
        expected_user_agent = '{}/{}'.format(self.app_name, '0.0.0')
        user_agent = self.test_class.session.headers['User-Agent']
        response = self.test_class.http_fetch('https://httpbin.org/get')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.test_class.session.headers['User-Agent'],
                          expected_user_agent)

    def test_user_agent_header_uses_application_not_version(self):
        test_class = flask_request.RequestsSession()

        response = self.test_class.http_fetch('https://httpbin.org/get')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.test_class.session.headers['User-Agent'],
                          test_class.headers['User-Agent'])

    def test_user_agent_uses_application_name_and_version(self):
        self.app.version = '1.0.0'
        user_agent = '{}/{}'.format(self.app_name, self.app.version)
        test_class = flask_request.RequestsSession(self.app)

        response = test_class.http_fetch('https://httpbin.org/get')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(test_class.session.headers['User-Agent'], user_agent)
