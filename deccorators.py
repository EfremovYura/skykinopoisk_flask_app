from flask import request
from flask_restx import abort
from container import auth_service
from functools import wraps

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        header_data = request.headers['Authorization']
        access_token = header_data.split("Bearer ")[-1]

        try:
            auth_service.check_token(access_token)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
