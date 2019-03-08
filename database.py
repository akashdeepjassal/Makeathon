import sqlite3
from sqlite3 import Error
import pathlib
import backend

logger = backend.get_logger()

db_path = str(pathlib.Path(__file__).resolve().parent) + '/db'
DB = db_path + '/app_data.db'

# Activating foreign keys
sql_activate_foreign_keys = "PRAGMA foreign_keys = ON;"

# By client I mean the ambulances that we have to dispatch over time
sql_create_client_table = """ CREATE TABLE IF NOT EXISTS client (
                                        device_id integer PRIMARY KEY,
                                        device_name text NOT NULL,
                                        authorization_token text NOT NULL,
                                        last_request_time text,
                                        last_dispatch_time text
                                        occupied integer DEFAULT 0
                                    ); """

sql_create_request_table = """ CREATE TABLE IF NOT EXISTS request (
                                        rowid integer PRIMARY KEY AUTOINCREMENT, 
                                        device_id integer,
                                        wsgi_environ text,
                                        url text NOT NULL,
                                        url_access_time text,
                                        access_route text,
                                        request_time text NOT NULL,
                                        request_scheme text, 
                                        request_addr text NOT NULL,
                                        request_method text,
                                        request_mimetype text,
                                        request_content_encoding text,
                                        user_agent text,  
                                        remote_user text,
                                        data text,
                                        host text,
                                        host_url text,
                                        FOREIGN KEY(device_id) REFERENCES client(device_id)
                                    ); """

sql_create_test_table = """ CREATE TABLE IF NOT EXISTS test (
                                        rowid integer PRIMARY KEY AUTOINCREMENT,
                                        data_received text
                                    ); """

sql_insert_into_client_table = """" INSERT INTO client(device_id, device_name, authorization_token, last_request_time, 
                                    last_dispatch_time) VALUES (?,?,?,?,?) """

sql_insert_into_request_table = """ INSERT INTO request(device_id, wsgi_environ, url, url_access_time, access_route, 
                                    request_time, request_scheme, request_addr, request_method, request_mimetype, 
                                    request_content_encoding, user_agent, remote_user, data, host, host_url) 
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

sql_insert_into_test_table = """ INSERT INTO test(data_received) VALUES (?)"""


def create_connection(db):
    """ create a database connection to a SQLite database """
    logger.info("Creating a connection with db...")
    try:
        conn = sqlite3.connect(db)
        logger.info('db connection created')
    except Error as e:
        logger.exception('Error occurred while creating connection')

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
    """
    try:
        c = conn.cursor()
        logger.info('Creating table...')
        c.execute(create_table_sql)
        logger.info('Table created')
    except Error as e:
        logger.error('Table not created')


def insert_into_client_table(conn, client):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_client_table, client)
        conn.commit()
        logger.info('DB write for client: {} success!'.format(repr(client)))
    except Error as e:
        logger.error('DB write for client: {} failed!'.format(repr(client)))


def insert_into_request_table(conn, request):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_client_table, request)
        conn.commit()
        logger.info('DB write for request: {} success!'.format(repr(request)))
    except Error as e:
        logger.error('DB write for request: {} failed!'.format(repr(request)))


def insert_into_test_table(conn, data):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_test_table, data)
        conn.commit()
        logger.info('DB write for test: {} success!'.format(repr(data)))
    except Error as e:
        logger.error('DB write for test: {} failed!'.format(repr(data)))


def activate_foreign_keys(conn):
    c = conn.cursor()
    c.execute(sql_activate_foreign_keys)


def initialize_db():
    backend.ensure_log_dir(db_path)
    conn = create_connection(DB)
    activate_foreign_keys(conn)
    create_table(conn, sql_create_client_table)
    create_table(conn, sql_create_request_table)
    create_table(conn, sql_create_test_table)
    conn.commit()


if __name__ == '__main__':
    initialize_db()
