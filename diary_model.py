import psycopg2

class db_model(object):
    connection=psycopg2.connect(dbname='mydiary', user='postgres', \
            host='localhost', password='01071992',port="5432")
    def create_table():
         
        connection=db_model.connection        
        
        cursor=connection.cursor()
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
        