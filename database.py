import sqlite3
from sqlite3 import Error, DatabaseError, OperationalError, InterfaceError, IntegrityError
import pathlib
import backend
import sys

logger = backend.get_logger()

db_path = str(pathlib.Path(__file__).resolve().parent) + '/db'
DB = db_path + '/app_data.db'

# Activating foreign keys
sql_activate_foreign_keys = "PRAGMA foreign_keys = ON;"

# Create statements: By client I mean the ambulances that we have to dispatch over time
sql_create_client_table = """ CREATE TABLE IF NOT EXISTS client (
                                        device_id text PRIMARY KEY,
                                        device_name text NOT NULL,
                                        authorization_token text NOT NULL,
                                        last_request_time text,
                                        last_dispatch_time text,
                                        occupied integer DEFAULT 0
                                    ); """

sql_create_request_table = """ CREATE TABLE IF NOT EXISTS request (
                                        rowid integer PRIMARY KEY AUTOINCREMENT, 
                                        device_id text,
                                        url text NOT NULL,
                                        url_access_date text,
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


# Insert statements
sql_insert_into_client_table = """ INSERT INTO client(device_id, device_name, authorization_token, last_request_time, 
                                    last_dispatch_time, occupied) VALUES (?, ?, ?, ?, ?, ?); """

sql_insert_into_request_table = """ INSERT INTO request(device_id, url, url_access_date, access_route, 
                                    request_time, request_scheme, request_addr, request_method, request_mimetype, 
                                    request_content_encoding, user_agent, remote_user, data, host, host_url) 
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """

sql_insert_into_test_table = """ INSERT INTO test(data_received) VALUES (?); """

# Drop tables
sql_drop_table_client = """ DROP TABLE client; """
sql_drop_table_request = """ DROP TABLE request; """
sql_drop_table_test = """ DROP TABLE test; """


def create_connection(db):
    """ create a database connection to a SQLite database """
    logger.info("Creating a connection with db...")
    try:
        conn = sqlite3.connect(db)
        logger.info('db connection created')
        return conn
    except Error as e:
        logger.exception('Error occurred while creating connection')

    return None


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
        logger.exception('Table not created')
        raise


def insert_into_client_table(conn, client):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_client_table, client)
        conn.commit()
        logger.info('DB write for CLIENT: {} success!'.format(repr(client)))
    except IntegrityError as e:
        logger.exception('IntegrityError while DB write for CLIENT: {} failed!'.format(repr(client)))
        raise
    except InterfaceError as e:
        logger.exception('InterfaceError while DB write for CLIENT: {} failed!'.format(repr(client)))
        raise
    except OperationalError as e:
        logger.exception('OperationalError while DB write for CLIENT: {} failed!'.format(repr(client)))
        raise
    except DatabaseError as e:
        logger.exception('DatabaseError while DB write for CLIENT: {} failed!'.format(repr(client)))
        raise
    except Error as e:
        logger.exception('Error while DB write for CLIENT: {} failed!'.format(repr(client)))
        raise


def insert_into_request_table(conn, request_data):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_request_table, request_data)
        conn.commit()
        logger.info('DB write for REQUEST: {} success!'.format(repr(request_data)))
    except IntegrityError as e:
        logger.exception('IntegrityError while DB write for REQUEST: {} failed!'.format(repr(request_data)))
        raise
    except InterfaceError as e:
        logger.exception('InterfaceError while DB write for REQUEST: {} failed!'.format(repr(request_data)))
        raise
    except OperationalError as e:
        logger.exception('OperationalError while DB write for REQUEST: {} failed!'.format(repr(request_data)))
        raise
    except DatabaseError as e:
        logger.exception('DatabaseError while DB write for REQUEST: {} failed!'.format(repr(request_data)))
        raise
    except Error as e:
        logger.exception('Error while DB write for REQUEST: {} failed!'.format(repr(request_data)))
        raise


def insert_into_test_table(conn, data):
    c = conn.cursor()
    try:
        c.execute(sql_insert_into_test_table, data)
        conn.commit()
        logger.info('DB write for TEST: {} success!'.format(repr(data)))
    except IntegrityError as e:
        logger.exception('IntegrityError while DB write for TEST: {} failed!'.format(repr(data)))
        raise
    except InterfaceError as e:
        logger.exception('InterfaceError while DB write for TEST: {} failed!'.format(repr(data)))
        raise
    except OperationalError as e:
        logger.exception('OperationalError while DB write for TEST: {} failed!'.format(repr(data)))
        raise
    except DatabaseError as e:
        logger.exception('DatabaseError while DB write for TEST: {} failed!'.format(repr(data)))
        raise
    except Error as e:
        logger.exception('Error while DB write for TEST: {} failed!'.format(repr(data)))


def drop_tables(conn):
    logger.info('Dropping tables...')
    c = conn.cursor()
    try:
        c.execute(sql_drop_table_client)
        c.execute(sql_drop_table_request)
        c.execute(sql_drop_table_test)
        conn.commit()
        conn.close()
    except IntegrityError as e:
        logger.exception('IntegrityError occurred while dropping tables!')
        raise
    except InterfaceError as e:
        logger.exception('InterfaceError occurred while dropping tables!')
        raise
    except OperationalError as e:
        logger.exception('OperationalError occurred while dropping tables!')
        raise
    except DatabaseError as e:
        logger.exception('DatabaseError occurred while dropping tables!')
        raise
    logger.info('Tables dropped')


def activate_foreign_keys(conn):
    c = conn.cursor()
    c.execute(sql_activate_foreign_keys)


def initialize_db():
    logger.info('Initializing database...')
    backend.ensure_log_dir(db_path)
    conn = create_connection(DB)
    activate_foreign_keys(conn)
    create_table(conn, sql_create_client_table)
    create_table(conn, sql_create_request_table)
    create_table(conn, sql_create_test_table)
    conn.commit()
    logger.info('Database initialized')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'drop_tables':
        conn = create_connection(DB)
        if conn is not None:
            drop_tables(conn)
            conn.close()
    initialize_db()
