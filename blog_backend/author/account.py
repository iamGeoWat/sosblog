from flask_restful import Resource, marshal, fields, reqparse
from ..common.db_connector.models import User
from werkzeug.security import generate_password_hash
from . import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'nickname': fields.String,
    'register_time': fields.DateTime,
    'is_admin': fields.Boolean
}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('nickname', type=str)

args = parser.parse_args()


class Account(Resource):
    def get(self, uid):
        q_user = User.query.get(uid)
        return marshal(q_user, user_fields)

    def put(self):
        q_user = User.query.filter(username=args['username'])
        q_user.password = generate_password_hash(args['password'])
        q_user.nickname = args['nickname']

        db.session.commit()
        return {'success': True, 'msg': 'Account modify success!'}
