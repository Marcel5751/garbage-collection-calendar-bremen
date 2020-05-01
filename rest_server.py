import main

import json
from datetime import datetime

import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Garbage Collector</h1><p>API to get Garbage Collection Dates</p>"


# A route to return all of the available entries in our catalog.
@app.route('/api/test', methods=['GET'])
def api_all():
    return json.dumps(dict(
        status="test_status",
        msg="test_tmsg",
    ))


# A route to return all of the available entries in our catalog.
@app.route('/api/garbageCalendar', methods=['GET'])
def getGarbageCalendar():
    if 'street' in request.args:
        street = str(request.args['street'])
    else:
        return "Error: No street field provided. Please specify a street."
    if 'number' in request.args:
        number = int(request.args['number'])
    else:
        return "Error: No number field provided. Please specify a number."

    args = {
        'number': number,
        'street': street,
        'start': datetime.now,
        'end': datetime.now
    }

    filename = main.garbage_calendar(args)

    return json.dumps(dict(
        status="success",
        msg="Created " + str(filename),
    ))


if __name__ == '__main__':
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        port=5001,
        threaded=True,
    )
    app.run(**flask_options)
