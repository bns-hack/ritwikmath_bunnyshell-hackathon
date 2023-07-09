from flask import Blueprint, request
import json

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.post('/subscriptions')
def create_subscriptions():
    try:
        data = request.json
        return f'{data}'
    except Exception as ex:
        return {'message': 'Something went wrong'}