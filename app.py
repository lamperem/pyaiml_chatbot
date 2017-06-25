#!/usr/bin/env python
from __future__ import print_function

from flask import Flask, redirect, url_for, render_template, session
from flask_socketio import emit, SocketIO
import argparse
import os
import aiml


app = Flask(__name__)
socketio = SocketIO(app)

k = aiml.Kernel()

@app.route('/')
def login():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/chat')
def chat():
  return render_template('chat.html')

@socketio.on('message', namespace='/ask')
def receive_message(message):
    ans=k.respond(message['data'])
    emit('response', {'data': ans.lower()})

if __name__ == '__main__':
    p = argparse.ArgumentParser("Twitter ML")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--aiml",default="aiml/mibot.aiml",type=str,
            action="store", dest="aiml",
            help="AIML file with rules [aiml/mibot.aiml]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()

    k.learn(opts.aiml)
    k.respond("load aiml b")

    socketio.run(app,
	    debug=opts.debug,
            host=opts.host,
            port=opts.port)
