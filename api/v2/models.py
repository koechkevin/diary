"""this module contains functions for database connection and create tables for the application
    """
import psycopg2

class DatabaseModel():
    """this class contains database structure for the application
    """
    connection = psycopg2.connect(dbname='mydiary', user='postgres', \
    host='localhost', password='01071992', port="5432")
    def create_table():
        """this function gets called in the main function of the run.py \
    files. It creates necessary tables for the project.
    do not alter any sql statement here
    """
        connection = DatabaseModel.connection
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users  \
        (ID SERIAL PRIMARY KEY, name VARCHAR NOT NULL, \
        email VARCHAR NOT NULL,Username VARCHAR NOT NULL,\
        password VARCHAR NOT NULL,  \
        registerdate TIMESTAMP default current_timestamp);")
        cursor.execute("create table if not exists entries \
        (entryID SERIAL PRIMARY KEY, title varchar NOT NULL, \
        entry text NOT NULL,ID int NOT NULL, \
        time TIMESTAMP default current_timestamp);")
        cursor.execute("create table IF NOT EXISTS blacklist \
        (token varchar PRIMARY KEY NOT NULL,time\
        TIMESTAMP default current_timestamp);")
        connection.commit()
        