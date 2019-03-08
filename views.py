from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info("User pinged {} endpoint".format(request.url))
    return render_template('index.html')


@app.route('/v1/current_state', methods=['POST'])
def get_current_state():
    app.logger.info("User pinged {} endpoint".format(request.url))
    pass


@app.route('/v1/test', methods=['GET'])
def test_url():
    app.logger.info("User pinged {} endpoint".format(request.url))
    data = request.args.get('test_data')
    if data is None:
        return 'API Parameter incorrect'
    else:
        return 'Data sent is: {}'.format(data)

