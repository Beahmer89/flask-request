import json
import requests
import urllib3

__version__ = '0.0.1'

DEFAULT_ACCEPT = 'application/json'
DEFAULT_CONTENT_TYPE = 'application/json'
DEFAULT_USER_AGENT = 'flask_request/{}'.format(__version__)
DEFAULT_TIMEOUT = 3


class RequestsSession(object):
    default_retry_codes = (429, 500, 502, 503, 504)
    headers = {'User-Agent': 'flask_request/1.0.0',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self, app=None, retries=3, backoff_factor=0.5,
                 status_forcelist=()):
        self.app = app
        self.status_forcelist = status_forcelist or self.default_retry_codes
        self.backoff_factor = backoff_factor
        self.retries = retries

        self.session = requests.Session()
        retry = urllib3.Retry(
            status=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist)

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['request'] = self

    def http_fetch(self, url,
                   method='GET',
                   headers={},
                   data=None,
                   timeout=DEFAULT_TIMEOUT):

        self.headers.update(headers)
        self._set_user_agent_header()
        self.session.headers.update(self.headers)

        body = self._http_serialize_request_data(data,
                                                 self.headers['Content-Type'])

        try:
            response = self.session.request(url=url,
                                            method=method,
                                            data=body,
                                            timeout=timeout)
        except requests.exceptions.RetryError as error:
            response = requests.Response()
            response.status_code = 599
            response.reason = "MAX RETRIES"
            response._content = b'{}'

        return response

    def _http_serialize_request_data(self, body, content_type):
        if not body or not isinstance(body, dict):
            return body

        if content_type == DEFAULT_CONTENT_TYPE:
            return json.dumps(body)
        raise ValueError('Unsupported Content-Type')

    def _set_user_agent_header(self):
        if hasattr(self.app, 'name'):
            name = self.app.name
            version = '0.0.0'
            if hasattr(self.app, 'version'):
                version = self.app.version

            self.headers['User-Agent'] = '{}/{}'.format(name, version)
