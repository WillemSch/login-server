from app import app
from flask import request
from flaskr.pygmentize_service import pygmentize
from json import dumps
from markupsafe import escape
from flaskr.database_service import search_messages, get_user_by_id, get_announcements, get_messages, get_message_by_id, get_user_by_name, add_message
from flask_login import login_required, current_user
import html


@app.get('/search')
@login_required
def search():
    user = current_user
    query = request.args.get('q') or request.form.get('q') or '*'
    rows = search_messages(query, user.id)
    result = ''
    for row in rows:
        row = list(row)
        row[1] = html.escape(get_user_by_id(row[1])[1])
        row[2] = html.escape(get_user_by_id(row[2])[1])
        result = f'{result}{dumps(row)}\n'
    return result


@app.route('/send', methods=['POST','GET'])
@login_required
def send():
    user = current_user
    recipient = request.args.get('recipient') or request.form.get('recipient')
    message = request.args.get('message') or request.args.get('message')
    if not recipient or not message:
        return f'ERROR: missing recipient or message'
    recipient = get_user_by_name(recipient)
    message = html.escape(message)
    if not recipient:
        return f'ERROR: Recipient does not exist'
    add_message(user.id, message, recipient[0])
    return 'ok'


@app.get('/announcements')
@login_required
def announcements():
    rows = get_announcements()
    anns = []
    for row in rows:
        anns.append({'sender':escape(row[0]), 'message':escape(row[1])})
    return {'data':anns}

