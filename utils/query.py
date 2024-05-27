from collections import namedtuple

from maams_be.settings import get_env_value

import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor


try:
    connection = psycopg2.connect(
        user=get_env_value("DB_USER"),
        password=get_env_value("DB_PASSWORD"),
        host=get_env_value("DB_HOST"),
        port=get_env_value("DB_PORT"),
        database=get_env_value("DB_NAME")
    )

    # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    '''
    Return all rows from a cursor as a namedtuple
    '''
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]


def query(query_str: str):
    '''
    Returns SELECT query result or number of rows modified
    by INSERT, UPDATE, DELETE queries if no error occured.
    Returns exception object if error does indeed occur.
    '''
    result = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        try:
            cursor.execute(query_str)
            if query_str.strip().upper().startswith("SELECT"):
                # Return SELECT query results if no error occured
                result = map_cursor(cursor)
            else:
                # Return number of rows modified by INSERT, UPDATE, DELETE if no error occured
                result = cursor.rowcount
                connection.commit()
        except Exception as e:
            # Handle errors that might pop up
            result = e

    return result
