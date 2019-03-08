import logging
import logging.handlers
import pathlib


def get_logger():
    logger = logging.getLogger('flask.app')
    logger.setLevel(logging.INFO)

    c_handler = logging.StreamHandler()
    f_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=20000, backupCount=3)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    # Create formatters and add to it handlers
    c_format = logging.Formatter('%(levelname)s in %(name)s: %(message)s')
    f_format = logging.Formatter('%(asctime)s | %(levelname)s in %(name)s [%(threadName)s]: %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    return logger


logger = get_logger()


def ensure_log_dir(path):
    logger.info('Creating {} directory...'.format(path))
    path = pathlib.Path(path)
    path.mkdir(parents=True, exist_ok=True)
    logger.info('{} directory created'.format(path))
