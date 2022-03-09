from psycopg import OperationalError, connect
import os


# import into data access layer

def create_connection():
    try:
        # create connection object
        # will implement environment variables in the configurations for these arguments
        conn = connect(
            host=os.environ.get("HOST"),
            dbname=os.environ.get("DBNAME"),
            user=os.environ.get("DBUSER"),
            password=os.environ.get("PASSWORD"),
            port=os.environ.get("PORT")
        )
        return conn
    except OperationalError as e:
        return str(e)


connection = create_connection()
