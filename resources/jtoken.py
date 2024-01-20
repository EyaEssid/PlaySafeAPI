from functools import wraps
from flask import request, jsonify
import jwt
from .config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "token is missing"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            usert = data['user']
            kwargs['usert'] = usert
        except:
            return jsonify({"message": "token is invalid"}), 400
        return f(*args, **kwargs)

    return decorated
