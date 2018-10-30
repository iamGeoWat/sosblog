import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from ..common.config import get_config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 获取配置信息
    app.config.from_object(get_config())

    db.init_app(app)

    # 注册blueprint
    from . import auth
    app.register_blueprint(auth.auth_blueprint)

    return app
