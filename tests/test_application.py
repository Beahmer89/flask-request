import unittest
import mock

from tests import fixtures

import flask_request


class TestApplication(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = fixtures.application()
        cls.test_client = app.test_client()

    def test_extension_installed(self):
        self.assertIsInstance(self.test_client.application.request,
                              flask_request.RequestsSession)
        self.assertEquals(self.test_client.application.request.retries, 1)
        self.assertIsInstance(
            self.test_client.application.extensions['request'],
            flask_request.RequestsSession)

    def test_extension_installed_and_works(self):
        response = self.test_client.get('/success')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json['external_service_data'],
                          fixtures.BODY['test_data'])

    def test_extension_installed_and_fails(self):
        response = self.test_client.get('/failure')
        self.assertEquals(response.status_code, 599)
        self.assertEquals(response.json['error_response'], 'MAX RETRIES')

    def test_extension_closes_session_after_request(self):
        with mock.patch('flask_request.RequestsSession.teardown') as teardown:
            app = fixtures.application()
            test_client = app.test_client()
            test_client.get('/success')

            self.assertEquals(teardown.call_count, 1)
