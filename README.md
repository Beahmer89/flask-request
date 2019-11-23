# flask-request
Flask extension for applications needing to handle responses within an application
and doubles as a mixin for client libraries.

## Installation
Fill in later

## Example
To use this as a flask extension do the following:
```python
from flask import Flask, current_app

app = Flask(__name__)
app.session = RequestsSession(app)

@app.route('/')
def hello_world():
    response = current_app.session.http_fetch('https://some.site.io/api')
    if not response.ok:
        abort(response.status_code)
    decoded_response = response.json()
    # Do stuff with json and render response
    data = {'Hello': 'World', 'other': decoded_response['key']}
    return data, 200
```

## Contributing
Set up your environment and run tests:
```bash
$ virtualenv --python=python3.7 env
(env) $ pip install requires/testing.txt
(env) $ nosetests -xvs tests
 ```
