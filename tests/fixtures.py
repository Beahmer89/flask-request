from flask import Flask, current_app
import json

from flask_request import RequestsSession


URL = 'https://httpbin.org/anything'
BODY = {'test_data': ['return','this','to', 'client']}

def application():
    app = Flask(__name__)
    app.request = RequestsSession(app)

    @app.route('/success', methods=['GET'])
    def external_post_test():
        response = current_app.request.http_fetch(URL, method='POST',
                                                  data=json.dumps(BODY))
        needed_data = []
        if response:
            needed_data = response.json()['json']['test_data']

        return {'external_service_data': needed_data}, 200

    return app
