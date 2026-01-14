import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="travel_ai",
        user="postgres",
        password="mypassword",
        host="localhost",
        port="5432"
    )
