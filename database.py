import sqlite3
from sqlite3 import Error
import backend

logger = backend.get_logger()

def create_connection(db):
    """ create a database connection to a SQLite database """
    logger.info("Creating a connection with db...")
    try:
        conn = sqlite3.connect(db)
        logger.info('db connection created')
    except Error as e:
        logger.exception('Error occurred while creating connection')
    finally:
        if conn is not None:
            conn.close()

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
    except Error as e:
        logger.error('Table not created')

    logger.info('Table created')
