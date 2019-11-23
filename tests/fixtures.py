from flask import Flask, current_app
import json

from flask_request import RequestsSession


URL = 'https://httpbin.org/anything'
URL2 = 'https://httpbin.org/status/500'
BODY = {'test_data': ['return','this','to', 'client']}

def application():
    app = Flask(__name__)
    app.request = RequestsSession(app, retries=1)

    @app.route('/success', methods=['GET'])
    def external_post_test():
        response = current_app.request.http_fetch(URL, method='POST',
                                                  data=json.dumps(BODY))
        needed_data = []
        if response:
            needed_data = response.json()['json']['test_data']

        return {'external_service_data': needed_data}, 200

    @app.route('/failure', methods=['GET'])
    def external_post_fail():
        response = current_app.request.http_fetch(URL2, method='PUT',
                                                  data=json.dumps(BODY))
        body = {}
        if not response.ok:
            body['error_response'] = response.reason
        return body, response.status_code,

    return app
