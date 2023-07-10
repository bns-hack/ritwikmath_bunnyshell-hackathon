from flask import Blueprint, request
import json
from controllers.customers import Customertroller
from controllers.plans import PlanController
from controllers.subscriptions import SubscriptionController

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.post('/subscriptions')
def create_subscriptions():
    return SubscriptionController().create()

@api_bp.get('/subscriptions')
def list_subscriptions():
    return SubscriptionController().list()

@api_bp.delete('/subscriptions/<id>')
def cancel_subscriptions(id):
    return SubscriptionController().cancel(id)

@api_bp.post('/plans')
def create_plan():
    return PlanController().create()

@api_bp.get('/plans')
def find_plans():
    return PlanController().index()

@api_bp.get('/me')
def loggedin_customer():
    return Customertroller().me()

@api_bp.post('/customers')
def create_customer():
    return Customertroller().create()

@api_bp.delete('/customers')
def delete_customer():
    return Customertroller().destroy()

@api_bp.get('/customers/setup-intent')
def customer_setup_intent():
    return Customertroller().setup_intent()