import jwt
from flask import request, jsonify, current_app
from my_util.my_logger import my_logger
from functools import wraps
import pymysql.cursors
conn = pymysql.connect(host='183.99.87.90',
        user='root',
        password='swhacademy!',
        db='Hee',
        charset='utf8')
cursor = conn.cursor()
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", '').split()

        invalid_msg = {
            'message': "Invalid Token. Registeration / authentication required",
            'authenticated': False
        }

        expired_msg = {
            'message': "expired Token. Reauthentication required",
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, 'qwersdaiofjhoqwihlzxcjvjl')
            parse_name = data['sub']
            sql = "SELECT ID FROM users WHERE ID = %s" % (parse_name)
            cursor.execute(sql)
            user = cursor.fetchone()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            my_logger.error(e)
            return jsonify(invalid_msg), 401

    return _verify