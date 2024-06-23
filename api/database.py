import mysql.connector
from mysql.connector import Error

def get_db_connection(db_config):
    try:
        connection = mysql.connector.connect(
            host=db_config['DB_HOST'],
            user=db_config['DB_USERNAME'],
            password=db_config['DB_PASSWORD'],
            database=db_config['DB_NAME'],
            port=db_config['DB_PORT']
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
