from werkzeug.wrappers import Request, Response, ResponseStream
from flask import Flask, jsonify, request
from typing import Any
import jwt
from os import getenv

class AuthMiddleware():
    def __init__(self, app) -> None:
        self.app = app

    def __call__(self, environ, start_response) -> Any:
        request = Request(environ)
        if "/api" in request.path:
            token = request.headers.get('Authorization')
            if not token:
                response = Response(u'Missing token', status=401, mimetype='application/json')
                return response(environ, start_response)
            else:
                token = token.split('Bearer ')[1]
            print(token)
            user = jwt.decode(token, getenv('JWT_SECRET'), algorithms=["HS256"])
            environ['loggedin_user'] = user
        return self.app(environ, start_response)