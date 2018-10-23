from flask import Flask
from .common.config import get_config

app = Flask(__name__)

_config = get_config()
app.config.from_object(_config)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
