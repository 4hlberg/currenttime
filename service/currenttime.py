from flask import Flask, request, Response
import os
import requests
import logging
import json
import dotdictify

app = Flask(__name__)
logger = None
format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = logging.getLogger('currenttime-rest-service')

# Log to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(logging.Formatter(format_string))
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


class DataAccess:

#main get function, will probably run most via path:path

    def __get_all_paged_entities(self, path, args):
        logger.info("Fetching data from url: %s", path)
        url = os.environ.get("base_url") + path
        req = requests.get(url, headers={"Accept":"Application/json", "Authorization": "Basic " + os.environ.get('basic_token')})

        if req.status_code != 200:
            logger.error("Unexpected response status code: %d with response text %s" % (req.status_code, req.text))
            raise AssertionError ("Unexpected response status code: %d with response text %s"%(req.status_code, req.text))
        res = dotdictify.dotdictify(json.loads(req.text))
        for entity in res['value']:

            yield(entity)
        logger.info('Returning entities')


    def get_entities(self,path, args):
        print("getting all entities")
        return self.__get_all_paged_entities(path, args)

data_access_layer = DataAccess()


def stream_json(entities):
    first = True
    yield '['
    for i, row in enumerate(entities):
        if not first:
            yield ','
        else:
            first = False
        yield json.dumps(row)
    yield ']'

@app.route("/<path:path>", methods=["GET", "POST"])
def get(path):
    entities = data_access_layer.get_entities(path, args=request.args)

    return Response(
        stream_json(entities),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))
