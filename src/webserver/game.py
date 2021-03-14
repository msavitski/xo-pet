import os
from flask import jsonify, request, Blueprint, Response, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from game_engine import GameEngine

DB_URL = os.environ['DB_DOCKER_URL']
DB_PORT = int(os.environ['DB_PORT'])
DB_USER = os.environ['POSTGRES_USER']
DB_PASS = os.environ['POSTGRES_PASSWORD']
DB = os.environ['POSTGRES_DB']
DB_SCHEMA = os.environ['POSTGRES_SCHEMA']

game = Blueprint('game', __name__)


@game.route('/game/start', methods=['PUT'])
@jwt_required
def start_game():
    """
    Webserver method for creating game instance

    Required JSON Parameters:
        user_id (str): user id
        row (int): count of row
        column (int): count of column

    Return:
        401: authentication false
        200: game create successfully
    """
    if request.data:
        GameEngine.start(user_id="user_id", c_row=3, c_column=3)
        return jsonify(game_id="UUID", character="X|O"), 200


@game.route('/game/move', methods=['POST'])
@jwt_required
def game_engine():
    """
        Webserver method for game move

        Required JSON Parameters:
            character (str): user character
            row (int): count of row
            column (int): count of column

        Return:
            401: authentication false
            200: json with fields (row, column, character)
    """
    if request.data:
        GameEngine.move(character="X", c_row=2, c_column=2)
        return jsonify(row=1,column=2,character="X|0"), 404


@game.route('/game/stats', methods=['PUT'])
@jwt_required
def get_users():
    """
       Webserver method for get game stats.
       JSON Parameters:
           game_id (str): game uuid
           user_id (int): user id
       Return:
           401: authentication false
           200: json with fields (user_id, game_result, game_time, count_move, count_win, count_lose)
    """
    if request.data:
        GameEngine.stats(game_id="uuid",user_id=2)
        return jsonify(), 200

