import functools
from flask import jsonify, g


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'success': False,
                            'msg': 'User not login'}, 401)

        return view(**kwargs)

    return wrapped_view


# def get_suc_json(msg, code=200):
#     json = dict()
#     json['success'] = True
#     json['code'] = code
#     json['msg'] = msg
#
#     return jsonify(json)
