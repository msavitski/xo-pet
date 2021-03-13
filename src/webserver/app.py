from flask import Flask, request, Response
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS
import json
import os


app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

from webserver.user import user as user_blueprint
app.register_blueprint(user_blueprint)

app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return Response(json.dumps("initial"), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443)
