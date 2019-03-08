from flask import Flask, render_template, request
import backend
import database

app = Flask(__name__)

logger = backend.get_logger()


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    return render_template('index.html')


@app.route('/v1/current_state', methods=['POST'])
def get_current_state():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    pass


@app.route('/v1/user/request')
def user_request():
    logger.info('User ip: {} accessed {} endpoint'.format(request.remote_addr, request.url))
    pass


@app.route('/v1/test', methods=['GET', 'POST', 'PUT'])
def test_url():
    logger.info("User ip: {} accessed {} endpoint".format(request.remote_addr, request.url))
    data = request.args.get('data')
    if data is None:
        return 'API Parameter incorrect'
    else:
        conn = database.create_connection(database.DB)
        database.insert_into_test_table(conn, (data,))
        return 'Data sent is: {}'.format(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
