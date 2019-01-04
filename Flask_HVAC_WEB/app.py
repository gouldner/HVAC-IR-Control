#!/usr/bin/python

import logging 
from logging.handlers import RotatingFileHandler
from datetime import datetime, time
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
import handler

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, time):
            return obj.isoformat()
        
        return obj.__dict__

class MyFlask(Flask):
    def make_response(self, rv):
        if hasattr(rv, 'response') and rv.response is None:
            return super(MyFlask, self).make_response(rv)
        if hasattr(rv, 'new_url') and rv.new_url is not None:
            return super(MyFlask, self).make_response(rv)
        return super(MyFlask, self).make_response(jsonify(rv))

app = MyFlask(__name__)
app.json_encoder = CustomJSONEncoder

@app.route('/config/', methods=['GET'])
def list_config():
    return handler.list_config(app)

@app.route('/hvac/off/', methods=['GET'])
def power_off():
    return handler.power_off(app)

@app.route('/hvac/on/', methods=['GET'])
def power_on():
    return handler.send_last_command(app)

@app.route('/hvac/command/', methods=['POST'])
def send_command():
    return handler.send_command(app, request.json)

@app.route('/last/command/', methods=['GET'])
def last_command():
    return handler.last_command(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4242)
