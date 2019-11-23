import unittest
from flask import Flask

from tests import fixtures


class TestApplication(unittest.TestCase):

    def setUp(self):
        app = fixtures.application()
        self.test_client = app.test_client()

    def test_extension_installed_and_works(self):
        response = self.test_client.get('/success')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json['external_service_data'],
                          fixtures.BODY['test_data'])
