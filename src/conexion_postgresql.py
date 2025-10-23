import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "123",
    "database": "portafolio_db",
}

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as ex:
        raise Exception(f"Error al conectar a la base de datos: {ex}")