import json
import requests
import urllib3

__version__ = '0.0.1'

DEFAULT_ACCEPT = 'application/json'
DEFAULT_CONTENT_TYPE = 'application/json'
DEFAULT_USER_AGENT = 'flask_request/{}'.format(__version__)
DEFAULT_TIMEOUT = 3


class RequestsSession(object):
    """ A Requests Session
    Used to take advantaged of requests configuration of adapters

    Provides defaults that are able to be overridden
    """
    default_retry_codes = (429, 500, 502, 503, 504)
    headers = {'User-Agent': 'flask_request/1.0.0',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self, app=None, retries=3, backoff_factor=0.5,
                 status_forcelist=()):
        """Initializes object with basic configurations for retries.

        :param Flask app: Flask application that will use this object
        :param int retires:
            Number of times to retry request on a bad status code
        :param float backoff_factor:
            Amount of time applied between retry attempts but only after the
            second try
        :param set status_forcelist:
            Set of status codes that retires will occur on
        """
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

    def http_fetch(self, url, method='GET', headers=None, params=None,
                   data=None, cookies=None, files=None, auth=None,
                   timeout=DEFAULT_TIMEOUT, allow_redirects=None, proxies=None,
                   hooks=None, stream=None, verify=None, cert=None):
        """Execute the request based on the given parameters.

        Will default to a GET request, update headers, set specific headers,
        and serialize data for the body if needed.

        Currently only supports application/json content-types and
        accept types.

        :param url: URL to send request to
        :param method: Name of method string
        :param headers:
            (optional) Number of times to retry request on a bad status code
        :param params:
            (optional) Dictionary of items to be sent in query string
        :param data:
            (optional) Dictionary of Request body
        :param cookies:
            (optional) Dictionary of cookies to be sent with request
        :param files:
            (optional) Dictionary of filename file-like-objects for upload
        :param auth:
            (optional) Auth tuple or callable to enable
        :param timeout:
            (optional) Time to wait to send data before giving up
        :param allow_redirects:
            (optional) Set to True by default
        :param proxies:
            (optional) Dictionary mapping protocol. See requests
        :param stream:
            (optional) Whether to immediately download the response content
        :param verify:
            (optional) Controls whether to verify the server's TLS certificate
        """

        if headers:
            self.headers.update(headers)
        self._set_user_agent_header()
        self.session.headers.update(self.headers)

        body = self._http_serialize_request_data(data,
                                                 self.headers['Content-Type'])

        try:
            response = self.session.request(url=url,
                                            method=method,
                                            data=body,
                                            cookies=cookies,
                                            files=files,
                                            auth=auth,
                                            timeout=timeout,
                                            allow_redirects=allow_redirects,
                                            proxies=proxies,
                                            stream=stream,
                                            verify=verify)
        except requests.exceptions.RetryError:
            response = requests.Response()
            response.status_code = 599
            response.reason = "MAX RETRIES"
            response._content = b'{}'

        return response

    def _http_serialize_request_data(self, body, content_type):
        """Serialize request body/data based on the content-type supplied by
        user.

        Currently only supports application/json

        :param body: Dictionary request body
        :param content_type: Content-Type of request
        """
        if not body or not isinstance(body, dict):
            return body

        if content_type == DEFAULT_CONTENT_TYPE:
            return json.dumps(body)
        raise ValueError('Unsupported Content-Type')

    def _set_user_agent_header(self):
        """Attempts to set the user-agent header if installed on application
        """
        if hasattr(self.app, 'name'):
            name = self.app.name
            version = '0.0.0'
            if hasattr(self.app, 'version'):
                version = self.app.version

            self.headers['User-Agent'] = '{}/{}'.format(name, version)
