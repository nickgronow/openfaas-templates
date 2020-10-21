#!/usr/bin/env python
from flask import Flask, request, jsonify
from waitress import serve
import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from function import handler

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

dns = "https://8f22032536a641d5b017e888e28073fd" "@o71452.ingest.sentry.io/5278583"
env = os.environ.get("APP_ENV", "development")
sentry_sdk.init(dns, integrations=[FlaskIntegration()], environment=env)


class Event:
    def __init__(self):
        if request.is_json:
            self.body = request.get_json()
        else:
            self.body = request.get_data()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path


class Context:
    def __init__(self):
        self.hostname = os.environ["HOSTNAME"]


def format_status_code(resp):
    if "code" in resp:
        return resp["code"]

    return 200


def format_body(resp):
    if "body" not in resp:
        return ""
    elif type(resp["body"]) == dict:
        return jsonify(resp["body"])
    else:
        return str(resp["body"])


def format_headers(resp):
    if "headers" not in resp:
        return []
    elif type(resp["headers"]) == dict:
        headers = []
        for key in resp["headers"].keys():
            header_tuple = (key, resp["headers"][key])
            headers.append(header_tuple)
        return headers

    return resp["headers"]


def format_response(resp):
    if resp is None:
        return ("", 200)

    statusCode = format_status_code(resp)
    body = format_body(resp)
    headers = format_headers(resp)

    return (body, statusCode, headers)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def call_handler(path):
    event = Event()
    context = Context()
    response_data = handler.handle(event, context)

    resp = format_response(response_data)
    return resp


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
