import json
from datetime import datetime

import flask
from flask import request, make_response, send_from_directory
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import main
import config_parser

app = flask.Flask(__name__)
auth = HTTPBasicAuth()
app.config["DEBUG"] = True


@auth.verify_password
def verify_password(username, password):
    if username == config_parser.credentials['username'] and \
            check_password_hash(config_parser.credentials['hashedPassword'], password):
        return username


@app.route('/', methods=['GET'])
def home():
    return "<h1>Garbage Collector</h1><p>API to get Garbage Collection Dates</p>"


# A route to return all of the available entries in our catalog.
@app.route('/api/test', methods=['GET'])
@auth.login_required
def api_all():
    return json.dumps(dict(
        status="test_status",
        msg="test_tmsg",
    ))


# A route to return all of the available entries in our catalog.
@app.route('/api/garbageCalendar', methods=['GET'])
@auth.login_required
def get_garbage_calendar():
    error_message = ""
    if request.args:
        if 'street' in request.args:
            street = str(request.args['street'])
        else:
            error_message = "Error: No street field provided. Please specify a street."
        if 'number' in request.args:
            number = str(request.args['number'])
        else:
            error_message = "Error: No number field provided. Please specify a number."
        if 'start' in request.args:
            start = int(request.args['start'])
        else:
            error_message = "Error: No start year provided."
        if 'end' in request.args:
            end = int(request.args['end'])
        else:
            error_message = "Error: No end year provided."
    else:
        error_message = "Error: No query parameters received"

    if error_message:
        return_json = json.dumps(dict(
            status=400,
            msg=error_message,
        ))
        resp = make_response(return_json, 400)
        headers = {'Content-Type': 'text/json'}
        resp.headers.extend(headers or {})
        return resp

    args = {
        'number': number,
        'street': street,
        'start': start,
        'end': end
    }

    resultDTO = main.get_garbage_calendar(args)

    return_json = json.dumps(dict(
        status=resultDTO.status_code,
        msg=resultDTO.result_messages,
    ))

    headers = {'Content-Type': 'text/json'}
    # status_code = flask.Response(status=200, property = return_json)
    resp = make_response(return_json, resultDTO.status_code)
    resp.headers.extend(headers or {})
    return resp


@app.route('/api/garbageCalendar/<filename>', methods=['GET'])
@auth.login_required
def get_file(filename):
    """Download the .ics file."""
    return send_from_directory("./ics-data", filename, as_attachment=True)


if __name__ == '__main__':
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        port=5001,
        threaded=True,
    )
    app.run(**flask_options)
