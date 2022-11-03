from app import app
from flask import abort, send_from_directory, make_response
from flaskr.auth_service import login_required
from pygments.formatters import HtmlFormatter

cssData = HtmlFormatter(nowrap=True).get_style_defs('.highlight')


@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    print('aa')
    return send_from_directory(app.root_path,
                               'templates/index.html', mimetype='text/html')


@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(app.root_path, 'flaskr/static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(app.root_path, 'flaskr/static/favicon.png', mimetype='image/png')


@app.get('/coffee/')
def nocoffee():
    abort(418)


@app.route('/coffee/', methods=['POST', 'PUT'])
def gotcoffee():
    return "Thanks!"


@app.get('/highlight.css')
def highlightStyle():
    resp = make_response(cssData)
    resp.content_type = 'text/css'
    return resp
