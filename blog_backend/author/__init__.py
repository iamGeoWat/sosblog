import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, Blueprint
from ..common.config import get_config
from flask_restful import Api

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 获取配置信息
    app.config.from_object(get_config())

    db.init_app(app)

    api_blueprint = Blueprint('api', __name__)

    api = Api(api_blueprint)

    from blog_backend.author.account import Account
    from blog_backend.author.article import Article
    from blog_backend.author.category import Category
    from blog_backend.author.comment import Comment
    api.add_resource(Account, '/account', '/account/<int:uid>')
    api.add_resource(Article, '/article', '/article/<int:aid>')
    api.add_resource(Category, '/category', '/category/<int:cid>')
    api.add_resource(Comment, '/comment')
    # api.add_resource(ArticleList, '/articles')

    # 注册蓝图
    app.register_blueprint(api_blueprint)
    from .auth import auth_blueprint
    from .article import articles_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(articles_blueprint)

    return app
