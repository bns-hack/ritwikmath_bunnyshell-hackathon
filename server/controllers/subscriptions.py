from flask import request
from models.subscriptions import SubscriptionsModel
from models.customers import CustomersModel
from facade.subscriptions import SubscriptionFacade
from databases.postgres import Postgres
import json

class SubscriptionController:
    def __init__(self) -> None:
        self.__model = SubscriptionsModel()

    def list(self):
        with Postgres().session.begin() as session:
            customer = CustomersModel().find_one(session, {'email': request.environ['loggedin_user']['email']})
            data = self.__model.find(session, {'customer_id': customer['id']})
            return json.loads(json.dumps({'message': 'Subscription list fetch successful', 'data': data}, default=str))

    def create(self):
        with Postgres().session.begin() as session:
            data = SubscriptionFacade(session).createSubscription(request.json)
            return json.loads(json.dumps({'message': 'Gateway Subscription Created', 'data': data}, default=str))