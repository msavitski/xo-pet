import psycopg2
import logging

from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


class ODDBDriver:
    def __init__(self, database_url, database_port, username, password, database, schema):
        self.database_url = database_url
        self.database_port = database_port
        self.username = username
        self.password = password
        self.database = database
        self.schema = schema
        self.connection = psycopg2.connect(user=username,
                                           password=password,
                                           host=database_url,
                                           port=database_port,
                                           database=database,
                                           options=f"-c search_path={self.schema}")

    def retrieve_user_by_identity(self, user_email=None):
        """ Retrieve user by email. If not presented any identity, return list of all users
            Parameters:
                user_email (str) : email
            Returns:
                user_info (dict): dict with fields : {_id:int, username:str, password:str} or list(user_info)
        """
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        if user_email is not None:
            query_return_dict = "select email,username,password from users where email = (%s);"
            query_values = (user_email,)
            cursor.execute(query_return_dict, query_values)
            user_info = cursor.fetchone()
        else:
            query_return_dict = "select * from users;"
            query_values = tuple("")
            cursor.execute(query_return_dict, query_values)
            user_info = cursor.fetchall()
        cursor.close()
        return user_info

    def create_new_user(self, user_info=None):
        """ Create new user
            Parameters:
                user_info (dict) : dict with fields : {name:str, email:str, password:str}
        """
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        insert_query = """INSERT INTO users (email, username, password)
                          VALUES (%(email)s, %(username)s, %(password)s) RETURNING id;"""
        cursor.execute(insert_query, user_info)
        user_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()
        return user_id

    def update_user_info(self, user_email=None, user_info=None):
        """ Update only user password by email or only full user info by user id
            Parameters:
                user_email(str): user email
                user_info (dict) : dict with fields : {username:str, email:str, password:str}
        """
        cursor = self.connection.cursor(cursor_factory=DictCursor)
        update_query = """"""
        cursor.execute(update_query, user_info)
        user_id = cursor.fetchone()[0]
        self.connection.commit()
        cursor.close()
        return user_id
