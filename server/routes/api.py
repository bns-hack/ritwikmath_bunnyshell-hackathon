from flask import Blueprint, request
import json
from controllers.plans import PlanController

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.post('/subscriptions')
def create_subscriptions():
    try:
        data = request.json
        return f'{data}'
    except Exception as ex:
        return {'message': 'Something went wrong'}

@api_bp.post('/plans')
def create_plan():
    return PlanController().create()

@api_bp.get('/plans')
def find_plans():
    return PlanController().index()