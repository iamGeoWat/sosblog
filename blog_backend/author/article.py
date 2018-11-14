from flask_restful import Resource, marshal, fields, reqparse
from ..common.db_connector.models import Article as Ar
from ..common.db_connector.models import User, Category
from .util import login_required
from . import db
from flask import g, Blueprint, session, jsonify

article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'content': fields.String,
    'create_time': fields.DateTime,
    'category': fields.String,
    'tags': fields.Nested({
        'id': fields.Integer,
        'tag_name': fields.String,
        'description': fields.String
    })
}

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Article must have a title')
parser.add_argument('content', type=str, help='Article must have its content')
parser.add_argument('category', type=int, help='Category is required')
parser.add_argument('tags', type=list, required=False)  # TODO action?

limit_parser = reqparse.RequestParser()
limit_parser.add_argument('limit', type=int, required=False)

articles_blueprint = Blueprint('articles', __name__, url_prefix='/articles')


class Article(Resource):
    def get(self, aid):
        q_article = Ar.query.get(aid)
        # q_category = Category.query.get(1)
        print(q_article)
        return marshal(q_article, article_fields)

    @login_required
    def post(self):
        """TODO"""
        args = parser.parse_args()
        author = g.user.id

        n_article = Ar(args['title'], author, args['content'], args['category'])

        db.session.add(n_article)
        db.session.commit()

        return {'success': True, 'msg': 'Article submit success'}

    @login_required
    def put(self):
        """TODO"""
        pass

    @login_required
    def delete(self, aid):
        """TODO"""
        pass


# class ArticleList(Resource):
#     def get(self):
#         q_articles = Ar.query.order_by(Ar.create_time).all()
#         print(User.query.get(q_articles[0].author))
#
#         results = marshal(q_articles, article_fields)
#         # 查询对应的author和category的名字
#         for article in results:
#             q_author_id = article['author']
#             q_category_id = article['category']
#             article['author'] = User.query.get(q_author_id).nickname
#             article['category'] = Category.query.get(q_category_id).cname
#
#         return results


@articles_blueprint.route('/all', methods=['get'])
def get_all_articles():
    """
    获取所有文章，默认获取前十篇
    """
    # 获取limit值，没有则默认为10
    args = limit_parser.parse_args()
    limit = args['limit']
    if limit is None:
        limit = 10

    q_articles = Ar.query.order_by(Ar.create_time).limit(limit).all()
    # print(User.query.get(q_articles[0].author))

    results = marshal(q_articles, article_fields)

    # 查询对应的author和category的名字 TODO:会不会有更加优雅的方法？
    for article in results:
        q_author_id = article['author']
        q_category_id = article['category']
        article['author'] = User.query.get(q_author_id).nickname
        article['category'] = Category.query.get(q_category_id).cname

    return jsonify(results)


@articles_blueprint.route('/<int:uid>', methods=['get'])
def get_user_articles(uid):
    """
    获取指定用户最近的文章，默认获取十篇
    """
    # 获取limit值，没有则默认为10
    args = limit_parser.parse_args()
    limit = args['limit']
    if limit is None:
        limit = 10

    q_articles = Ar.query.filter_by(author=uid).order_by(Ar.create_time).limit(limit).all()

    results = marshal(q_articles, article_fields)

    # 查询对应的author和category的名字 TODO:会不会有更加优雅的方法？
    for article in results:
        q_author_id = article['author']
        q_category_id = article['category']
        article['author'] = User.query.get(q_author_id).nickname
        article['category'] = Category.query.get(q_category_id).cname

    return jsonify(results)


@articles_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)