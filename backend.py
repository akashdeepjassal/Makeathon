import sqlite3
from sqlite3 import Error
import logging


def get_logger():
    logger = logging.getLogger('flask.app')
    logger.setLevel(logging.INFO)

    c_handler = logging.StreamHandler()
    f_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=20000, backupCount=3)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


logger = get_logger()


def create_connection(db):
    """ create a database connection to a SQLite database """
    logger.info("Creating a connection with db...")
    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
        logger.info('db connection created')
    except Error as e:
        logger.exception('Error occurred while creating connection')
        print(e)
    finally:
        if conn is not None:
            conn.close()

    return conn


