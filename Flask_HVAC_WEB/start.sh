#!/bin/bash
gpio write 17 0
gpio export 17 out
FLASK_APP=app.py
# Note: --host=0.0.0.0 allows connection on host ip instead of just localhost
#sudo flask run --host=0.0.0.0
flask run --host=0.0.0.0 &> flask.log
