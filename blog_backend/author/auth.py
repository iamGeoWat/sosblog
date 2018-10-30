from flask import Blueprint, request, session, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from ..common.db_connector.models import User
from . import db
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['post'])
def login():
    """
    用户登录

    参数：
    {
        'username': 'USERNAME',
        'password': '123'
    }
    """
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username)

    if not user:
        return jsonify({'success': False,
                        'msg': 'Username not exist!'})

    if not check_password_hash(user.password, password):
        return jsonify({'success': False,
                        'msg': 'Incorrect password!'})

    session.clear()
    session['user_id'] = user.id

    return jsonify({'success': True,
                    'msg': 'Login success'})


@auth_blueprint.route('/register', methods=['post'])
def register():
    """
    用户注册

    参数：
    {
        'username': 'NEW_USERNAME',
        'password': '123',
        'nickname': 'NICKNAME'
    }
    """
    n_username = request.json.get('username')
    if User.query.filter_by(username=n_username):
        return jsonify({'success': False,
                        'msg': 'Username already exists!'})

    password_hash = generate_password_hash(request.form['password'])

    n_user = User(n_username, password_hash, request.form['nickname'])
    db.session.add(n_user)

    return jsonify({'success': True,
                    'msg': 'Register success!'})


@auth_blueprint.route('/check_username_existence', methods=['post'])
def check_username_existence():
    """
    检查用户名是否存在

    参数：
    {
        'username': 'USERNAME_TO_CHECK'
    }
    """
    n_username = request.json.get('username')
    if User.query.filter_by(username=n_username):
        return jsonify({'isExisted': True})
    else:
        return jsonify({'isExisted': False})


@auth_blueprint.route('/logout')
def logout():
    """
    用户登出
    """
    session.clear()
    return jsonify({'success': True,
                    'msg': 'Logout success'})


@auth_blueprint.before_app_request()
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
