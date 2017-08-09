import os
from flask import Flask, request, jsonify, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
