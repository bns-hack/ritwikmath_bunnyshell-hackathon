from flask import request
from models.subscriptions import SubscriptionsModel
from models.customers import CustomersModel
from models.plans import PlansModel
from facade.subscriptions import SubscriptionFacade
from databases.postgres import Postgres
import json

class SubscriptionController:
    def __init__(self) -> None:
        self.__model = SubscriptionsModel()

    def list(self):
        with Postgres().session.begin() as session:
            data = None
            customer = CustomersModel().find_one(session, {'email': request.environ['loggedin_user']['email']})
            if customer:
                data = self.__model.find(session, {'customer_id': customer['id']})
                for subs in data:
                    subs['plan_name'] = PlansModel().find_one(session, {'id': subs['plan_id']})['name']
            return json.loads(json.dumps({'message': 'Subscription list fetch successful', 'data': data}, default=str))

    def create(self):
        with Postgres().session.begin() as session:
            data = SubscriptionFacade(session).createSubscription(request.json)
            return json.loads(json.dumps({'message': 'Subscription Created', 'data': data}, default=str))
    
    def cancel(self, sub_id):
        with Postgres().session.begin() as session:
            data = SubscriptionFacade(session).cancelSubscription({'sub_id': sub_id})
            return json.loads(json.dumps({'message': 'Subscription Cancelled', 'data': data}, default=str))