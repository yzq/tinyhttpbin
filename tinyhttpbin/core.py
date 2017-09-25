import os

import time
import uuid

from flask import Flask, request, jsonify, render_template, make_response, url_for, Response, jsonify as flask_jsonify
from werkzeug.http import http_date
from werkzeug.utils import redirect

from helper import multidict_to_dict, ROBOT_TXT, ANGRY_ASCII, get_headers


def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b'\n'):
        response.data += b'\n'
    return response


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robot.txt')
def view_robot_page():
    response = make_response()
    response.data = ROBOT_TXT
    # response.content_type = 'text/plain'
    response.headers['Content-Type'] = 'text/plain'
    return response


@app.route('/deny')
def view_deny_page():
    response = make_response()
    response.data = ANGRY_ASCII
    response.content_type = 'text/plain'
    return response


@app.route('/ip')
def view_origin():
    """Returns Origin IP."""

    return jsonify(origin=request.headers.get('X-Forwarded-For', request.remote_addr))


@app.route('/user-agent')
def view_user_agent():
    """Returns User-Agent"""

    headers = get_headers()
    return jsonify({'user-agent': headers['user-agent']})
    # user_agent = request.headers.get('User-Agent')
    # return jsonify({'user-agent': user_agent})


@app.route('/headers')
def view_headers():
    headers = request.headers.items()
    return jsonify({'headers': dict(headers)})


@app.route('/get', methods=('GET',))
def view_get():
    headers = request.headers.items()
    url = request.url
    args = multidict_to_dict(request.args)
    print type(args)
    print args
    return jsonify({'headers': dict(headers), 'url': url, 'args': args})


@app.route('/cookie/set/<name>/<value>')
def set_cookie(name, value):
    r = make_response(redirect(url_for('view_cookies')))
    r.set_cookie(key=name, value=value)
    return r


@app.route('/cookies/set')
def set_cookies():
    cookies = dict(request.args.items())
    r = make_response(redirect(url_for('view_cookies')))
    for k, v in cookies.items():
        r.set_cookie(key=k, value=v)

    return r


@app.route('/cookies')
def view_cookies():
    cookies = dict(request.cookies.items())
    return jsonify(cookies=cookies)


@app.route('/response-headers', methods=['GET', 'POST'])
def response_headers():
    args = multidict_to_dict(request.args)
    print args
    j = jsonify({'headers': args})
    return j


@app.route('/redirect-to', methods=['GET', 'POST'])
def redirect_to():
    location = request.args['url']
    return make_response(redirect(location))


@app.route('/delay/<delay>')
def delay_response(delay):
    delay = min(float(delay), 10)
    time.sleep(delay)
    headers = request.headers.items()
    return jsonify({'headers': dict(headers)})


@app.route('/image/jpeg')
def image_jpeg():
    data = resource('images/jackal.jpg')
    return Response(data, headers={'Content-Type': 'image/jpeg'})


def resource(filename):
    path = os.path.join(tmpl_dir, filename)
    return open(path, 'rb').read()


@app.route('/xml')
def xml():
    data = resource('sample.xml')
    return Response(data, headers={'Content-Type': 'application/xml'})


@app.route('/cache', methods=('GET',))
def view_cache():
    is_conditional = request.headers.get('If-Modified-Since') or request.headers.get('If-None-Match')
    response = make_response()
    print response.headers.__class__.__name__
    if not is_conditional:
        response.headers['Last-Modified'] = http_date()
        response.headers['Etag'] = uuid.uuid4().hex
    else:
        response.status_code = 304

    return response


@app.route('/cache/<int:value>', methods=('GET',))
def cache_control(value):
    response = make_response()
    response.headers['Cache-Control'] = 'max-age={0}'.format(value)
    return response


if __name__ == '__main__':
    app.run(debug=True)
