from flask import Flask, request, Response
import os
import requests
import logging
import sys
import json
import dotdictify

app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('cvpartner-rest-service')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


@app.route("/<path:path>", methods=["GET", "POST"])
def employee_methods(path):
    if request.method == "POST":
        post_url = os.environ.get('base_url') + path
        logger.info(request.get_json())
        entities = request.get_json()
        headers = json.loads(os.environ.get('headers').replace("'", "\""))
        logger.info('Sending entites to %s', path)
        response = requests.post(post_url, data=entities, headers=headers)
        if response.status_code is not 200:
            logger.error("Got error code: " + str(response.status_code) + "with text: " + response.text)
            return Response(response.text, status=response.status_code, mimetype='application/json')
        logger.info("Prosessed " + str(len(entities)) + " entities")
        return Response(response.text, status=response.status_code, mimetype='application/json')

    elif request.method == "GET":
        logger.info("wrong method")
    else:
        sys.exit()
    return Response(entities)


    # Will be taken in to use later, next iteration after test
    # return Response(
    #     stream_json(entities),
    #     mimetype='application/json'
    # ){AttributeError}'str' object has no attribute 'items'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))
