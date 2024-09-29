import psycopg2
from dotenv import dotenv_values

config = dotenv_values('.env')

def get_db_connection():
    return psycopg2.connect(
        host = "localhost",
        dbname = "postgres",
        user = config['USER'],
        password=config['PASSWORD']
    )

