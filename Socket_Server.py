#!/usr/bin/python
# -*- coding: utf-8 -*-

import eventlet.wsgi
from flask import Flask
import socketio
import json
# from flask_socketio import SocketIO
sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def on_connect(sid, environ):
    print("connect OK")
    # print("client： ", sid, "Link Sever Already!")


@sio.on('client_sent_message')
def on_revieve(message, data):
    if data:
        # print('From Client Get Message : %s' % data['messageInput'])
        # send_message_to_client('You sent ' + data['messageInput'] + ' to server. Server sucessfully recieved.')
        send_message_to_client(data['messageInput'])
    else:
        print("OK")
        # print('Get Null Message!')

@sio.on('client_update_message')
def update_revieve(message, data):
    if data:
        # print('From Client Get Message : %s' % data['messageInput'])
        # send_message_to_client('You sent ' + data['messageInput'] + ' to server. Server sucessfully recieved.')
        word = send_message_data(data['_updateData'])
        # print(word)
        print("OK啦")
    else:
        # print("OK")
        print('Get Null Message!')

# 伺服器到客戶端
def send_message_to_client(_messageInput):
    sio.emit(
        'server_sent_message',
        data={'messageInput': _messageInput},
        skip_sid=True)

def send_message_data(_updateData):
    with open("User_Online.json", mode="r", encoding="utf-8") as f:
        data = json.load(f)
        data1 = json.dumps(data)
        print("檔案已傳送!")
        sio.emit(
            'server_update_message',
            data={'my_data': str(data1) },
            skip_sid=True)


# region 聊天室系統
@sio.on('client_sent_chatText')
def on_revieve(chatText, data):
    if data:
        # print('From Client Get Word : %s' % data['chatTextInput'])
        # send_message_to_client('You sent ' + data['messageInput'] + ' to server. Server sucessfully recieved.')
        send_chatText_to_client(data['chatTextInput'])
    else:
        # print("OK")
        print('Get Null Word!')


def send_chatText_to_client(_chatTextInput):
    sio.emit(
        'server_sent_chatText',
        data={'chatTextInput': _chatTextInput},
        skip_sid=True)


# endregion

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)