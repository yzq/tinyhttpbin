import os

import time
from flask import Flask, request, jsonify, render_template, make_response, url_for, Response
from werkzeug.utils import redirect

from helper import multidict_to_dict

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user-agent')
def view_user_agent():
    user_agent = request.headers.get('User-Agent')
    print type(request)
    print "__dict__:"
    print request.headers.__dict__
    print "items():"
    print request.headers.items()
    print "request"
    print request.__dict__
    return jsonify({'user-agent': user_agent})


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


if __name__ == '__main__':
    app.run(debug=True)
