from flask_restful import Resource, marshal, fields, reqparse
from ..common.db_connector.models import Article as Ar

article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'content': fields.String,
    'create_time': fields.DateTime,
    'category': fields.String,  # TODO 只能查询出category.id
    'tags': fields.Nested({
        'id': fields.Integer,
        'tag_name': fields.String,
        'description': fields.String
    })
}

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)
parser.add_argument('category', type=int)
parser.add_argument('tags', type=dict)  # TODO action?


class Article(Resource):
    def get(self, aid):
        q_article = Ar.query.get(aid)
        # q_category = Category.query.get(1)
        print(q_article)
        return marshal(q_article, article_fields)

    def post(self):
        """TODO"""
        args = parser.parse_args()
        pass

    def put(self):
        """TODO"""
        pass

    def delete(self):
        """TODO"""
        pass
