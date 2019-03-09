from flask import Flask, render_template, request
import backend
import database
from datetime import datetime
from sqlite3 import Error

app = Flask(__name__)

logger = backend.get_logger()

pages = {'home': '/', 'current state': '/v1/current_state', 'request ambulance': '/v1/user/request'}


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    return render_template('index.html', pages=pages)


# api for current state of devices
@app.route('/v1/current_state', methods=['GET', 'POST'])
def get_current_state():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    request_dict = dict()
    device_id = request.args.get('id')
    if device_id is not None:
        request_dict['device_id'] = str(device_id)
    else:
        request_dict['device_id'] = ""
    request_dict['url'] = str(request.url)
    request_dict['url_access_date'] = str(datetime.now())
    request_dict['access_route'] = str(request.access_route)
    request_dict['request_time'] = ""   # TODO: Add this
    request_dict['request_scheme'] = str(request.scheme)
    request_dict['request_addr'] = str(request.remote_addr)
    request_dict['request_method'] = str(request.method)
    request_dict['request_mimetype'] = str(request.mimetype)
    request_dict['request_content_encoding'] = str(request.content_encoding)
    request_dict['user_agent'] = str(request.user_agent)
    request_dict['remote_user'] = str(request.remote_user)
    request_dict['data'] = str(request.data)
    request_dict['host'] = str(request.host)
    request_dict['host_url'] = str(request.host_url)

    request_tuple = ()
    for key in request_dict:
        request_tuple = request_tuple + (request_dict[key], )

    # adding data to database
    try:
        conn = database.create_connection(database.DB)
        database.insert_into_request_table(conn, request_tuple)
        conn.close()
    except Error as e:
        logger.exception('DB write failed for REQUEST since the user is not registered. User: {}'.format(request_tuple))
        return 'ERR_UNREGISTERED: User not registered'

    if request_dict['device_id'] == "":
        request_dict['device_id'] = 'No Device: Accessing from a website'

    if request.method == 'GET':
        return render_template('current_state.html', request=request_dict)
    else:
        return str(request_dict)


# api for users so that can request an ambulance
@app.route('/v1/user/request', methods=['GET', 'POST'])
def user_request():
    logger.info('User ip: {} accessed {} endpoint'.format(request.remote_addr, request.url))
    pass


@app.route('/v1/ambulance/register', methods=['POST'])
def client_ambulance():
    logger.info('User ip: {} accessed {} endpoint'.format(request.remote_addr, request.url))
    client = dict()
    id = request.args.get('id')
    name = request.args.get('name')
    token = request.args.get('authorization_token')
    if id is not None:
        client['device_id'] = id
    else:
        return "Incomplete registration parameters"
    if name is not None:
        client['device_name'] = name
    else:
        return "Incomplete registration parameters"
    if token is not None:
        client['authorization_token'] = token
    else:
        return "Incomplete registration parameters"
    client['last_request_time'] = str(datetime.now())
    client['last_dispatch_time'] = ""
    client['occupied'] = 0

    client_tuple = ()

    for key in client:
        client_tuple = client_tuple + (client[key], )

    # adding data to database
    try:
        conn = database.create_connection(database.DB)
        database.insert_into_client_table(conn, client_tuple)
        conn.close()
    except Error as e:
        logger.exception('DB write failed for CLIENT and the user is not registered. User: {}'.format(client_tuple))
        return 'ERR_UNREGISTERED: User not registered'

    return 'Client ambulance registration is successful'


@app.route('/v1/test', methods=['GET', 'POST', 'PUT'])
def test_url():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    data = request.args.get('data')
    if data is None:
        return 'API Parameter incorrect'
    else:
        try:
            conn = database.create_connection(database.DB)
            database.insert_into_test_table(conn, (data,))
            return 'Data sent is: {}'.format(data)
        except Error as e:
            logger.info('DB write failed for TEST')
            return 'ERR_DB: Data could not be written to database.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
