from flask import request, jsonify
from flask_login import login_required, current_user
from app import app
from flaskr.database_service import *
import html


@app.post('/new')
@login_required
def new():
    user = current_user
    recipient = request.args.get('recipient') or request.form.get('recipient')
    message = request.args.get('message') or request.form.get('message')
    if not recipient or not message:
        return jsonify(Error='Recipient or message is missing.'), 400
    recipient = get_user_by_name(recipient)
    message = html.escape(message)
    if not recipient:
        return jsonify(Error='Recipient or message is missing.'), 400
    add_message(user.id, message, recipient[0])
    return {}, 200


@app.route('/messages', methods=['GET'])
@login_required
def messages():
    user = current_user
    rows = get_messages(user.id)
    messages = []
    for row in rows:
        row = list(row)
        row[1] = html.escape(get_user_by_id(row[1])[1])
        row[2] = html.escape(get_user_by_id(row[2])[1])
        messages.append({'id':row[0], 'sender':row[1], 'recipient':row[2], 'message':row[4]})
    return jsonify(messages=messages), 200


@app.route('/messages/<message_id>', methods=['GET'])
@login_required
def message_by_id(message_id):
    print(message_id)
    user = current_user
    message = get_message_by_id(message_id, user.id)
    if message:
        return jsonify(
            id=message[0],
            sender=get_user_by_id(message[1])[1],
            recipient=get_user_by_id(message[2])[1],
            message=message[4]
        ), 200
    else:
        return {}, 200
