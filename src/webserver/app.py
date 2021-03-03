from flask import Flask, request, Response
from flask_cors import CORS
import json


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return Response(json.dumps("initial"), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443)
