import datetime
import time
from os import abort
from typing import Dict, List, Union

from flask import Flask, request

app: Flask = Flask(__name__)

messages = [
    {'username': "KEK", 'text': 'Hello', 'time': 0.0}
]
users = {
    'jojo': '123'
}


@app.route("/")
def hello():
    return "Hello, world!"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Messenger',
        'time': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'messages_count': len(messages),
        'users_count': len(users)
    }


@app.route("/send", methods=['POST'])
def send():
    username = request.json['username']
    password = request.json['password']

    if username in users:
        if password !=users[username]:
            return abort(401)
        else:
            users[username] = password

    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)

    print(messages)

    return {'ok': True}


@app.route("/messages")
def messages_view():
    after = float(request.args.get('after'))

    filtered_messages = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered_messages
    }


app.run()
