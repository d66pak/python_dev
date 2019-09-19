from flask import Flask
from flask import jsonify
app = Flask(__name__)


@app.route('/<username>', methods=['GET'])
def hello_world(username):
    response = {
        'message': 'Hello, {u}!'.format(u=username)
    }
    resp = jsonify(response)
    resp.status_code = 200
    return resp
