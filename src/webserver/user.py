import os
from flask import jsonify, request, Blueprint, Response, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from db.postgres_connector import ODDBDriver

DB_URL = os.environ['DB_DOCKER_URL']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']
DB = os.environ['POSTGRES_DB']
DB_SCHEMA = os.environ['POSTGRES_SCHEMA']

user = Blueprint('user', __name__)


@user.route('/user/register', methods=['POST'])
def create_user():
    """
    Webserver method for creating user instance from request json

    Required JSON Parameters:
        email (str): user email
        name (str): user name
        password (str): user password

    Return:
        409: user already exists
        200: user create successfully
    """
    if request.data:
        email = request.get_json()['email'].lower()
        db_connector = ODDBDriver(DB_URL, DB_PORT, DB_USER, DB_PASS, DB, DB_SCHEMA)
        exist_user = db_connector.retrieve_user_by_identity(user_email=email)
        if exist_user:
            return jsonify(message="User Already Exist"), 409  # conflict
        name = request.get_json()["username"]
        password = generate_password_hash(request.get_json().get("password"))
        user_info = dict(username=name, email=email, password=password)
        user_id = db_connector.create_new_user(user_info=user_info)
        return jsonify(message="User created successfully", id=user_id), 200


@user.route('/user/update', methods=['PUT'])
@jwt_required
def update_user():
    """
        Webserver method for update user information using request json

        Required JSON Parameters:
            email (str): user email
            name (str): user name
            password (str): user password

        Return:
            401: authentication false
            404: incorrect user email
            200: user update successfully
    """
    if request.data:
        email = request.get_json().get("email")
        db_connector = ODDBDriver(DB_URL, DB_PORT, DB_USER, DB_PASS, DB, DB_SCHEMA)
        exist_user = db_connector.retrieve_user_by_identity(user_email=email)
        if exist_user:
            email = request.get_json().get('email').lower()
            name = request.get_json().get("name")
            password = request.get_json().get("password")
            user_info = dict(email=email, username=name,
                                password=password)
            # TODO WIP skip missing values on update
            user_id = db_connector.update_user_info(user_email=email, user_info=user_info)
            current_app.logger.info(f"Updated information for {user_id}")
            return jsonify(message=f"Updated information for {user_id}"), 200
        else:
            return jsonify(message="User not found"), 404


@user.route('/user/get', methods=['PUT'])
@jwt_required
def get_users():
    """
           Webserver method for get users information.
           If email on request, retrieve user info by email
           Optional JSON Parameters:
               email (str): user email
           Return:
               401: authentication false
               404: incorrect user email
               200: user info
    """
    check_email = request.get_json().get("email")
    db_connector = ODDBDriver(DB_URL, DB_PORT, DB_USER, DB_PASS, DB, DB_SCHEMA)
    if check_email is not None:
        exist_user = db_connector.retrieve_user_by_identity(user_email=check_email)
        if exist_user:
            return jsonify(db_connector.retrieve_user_by_identity(user_email=check_email)), 200
        else:
            return jsonify(message="Incorrect user email"), 404
    else:
        return jsonify(db_connector.retrieve_user_by_identity()), 200


@user.route("/user/login", methods=["POST"])
def login():
    """
        Webserver method for login.

        Required JSON Parameters:
            email (str): user email
            password (str): user password

        Return:
            401: authentication false
            404: incorrect email
            200: login successfully. Return token as access_token
            :return:
        """
    if request.data:
        email = request.get_json().get("email").lower()
        password = request.get_json().get("password")
        db_connector = ODDBDriver(DB_URL, DB_PORT, DB_USER, DB_PASS, DB, DB_SCHEMA)
        exist_user = db_connector.retrieve_user_by_identity(user_email=email)
        current_app.logger.error(exist_user)
        if exist_user:
            if check_password_hash(exist_user["password"], password):
                expires = timedelta(hours=4)
                access_token = create_access_token(identity=email, expires_delta=expires)
                exist_user = db_connector.retrieve_user_by_identity(user_email=email)
                return jsonify(data=exist_user, authenticated=True, access_token=access_token), 200
            else:
                return jsonify(authenticated=False), 401
        else:
            return jsonify(message="Incorrect user email"), 404
