from flask import Flask, render_template, request
import backend

app = Flask(__name__)

logger = backend.get_logger()


@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info("User pinged {} endpoint".format(request.url))
    return render_template('index.html')


@app.route('/v1/current_state', methods=['POST'])
def get_current_state():
    logger.info("User pinged {} endpoint".format(request.url))
    pass


@app.route('/v1/test', methods=['GET', 'POST', 'PUT'])
def test_url():
    logger.info("User pinged {} endpoint".format(request.url))
    data = request.args.get('test_data')
    if data is None:
        return 'API Parameter incorrect'
    else:
        return 'Data sent is: {}'.format(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
