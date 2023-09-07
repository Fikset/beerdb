#!/usr/bin/env python3

from flask import Flask, request
from prometheus_client import generate_latest, Summary

app = Flask(__name__)


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


# Decorate function with metric.
@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
@REQUEST_TIME.time()
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route("/health", methods=["GET"])
@REQUEST_TIME.time()
def echo_ok():
    return "OK"

@app.route("/metrics", methods=["GET"])
@REQUEST_TIME.time()
def echo_requests():
    return generate_latest()
