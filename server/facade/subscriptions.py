from flask import request
from datetime import datetime
from payment_gateway.PaymentGatewayFactory import PaymentgatewayFactory
from models.customers import CustomersModel
from models.plans import PlansModel
from models.subscriptions import SubscriptionsModel

class SubscriptionFacade:
    def __init__(self, session) -> None:
        self.session = session

    def createSubscription(self, arg):
        gateway = PaymentgatewayFactory.create_payment_gateway(arg.get('gateway'))
        plan_id = arg.pop('plan_id')
        email = request.environ.get('loggedin_user').get('email')
        plan = PlansModel().find_one(self.session, {
            'id': plan_id
        })
        customer = self.createCustomer({
            'gateway': arg.get('gateway'),
            'email': email
        })
        if customer:
            data = gateway.createSubscription({
                'customer': customer['gateway_cust_id'],
                'items': [
                    {"price": plan['gateway_price_id']},
                ],
                'default_payment_method': arg.get('payment_method')
            })
            amount = 0
            for item in data['items']['data']:
                amount += (int(item['quantity']) * int(item['price']['unit_amount']))/100
            subscription = SubscriptionsModel().insert_one(self.session, {
                'customer_id': customer['id'],
                'gateway': arg.get('gateway'),
                'gateway_sub_id': data['id'],
                'cancel_at': data['cancel_at'] and datetime.fromtimestamp(data['cancel_at']) or data['cancel_at'],
                'cancel_at_period_end': data['cancel_at_period_end'] and datetime.fromtimestamp(data['cancel_at_period_end']) or data['cancel_at_period_end'],
                'canceled_at': data['canceled_at'] and datetime.fromtimestamp(data['canceled_at']) or data['canceled_at'],
                'created_at': data['created'] and datetime.fromtimestamp(data['created']) or data['created'],
                'started_at': data['start_date'] and datetime.fromtimestamp(data['start_date']) or data['start_date'],
                'currency': data['currency'],
                'status': data['status'],
                'current_period_start': data['current_period_start'] and datetime.fromtimestamp(data['current_period_start']) or data['current_period_start'],
                'current_period_end': data['current_period_end'] and datetime.fromtimestamp(data['current_period_end']) or data['current_period_end'],
                'amount': amount,
                'plan_id': plan_id,
            })
        return subscription

    def createCustomer(self, arg):
        gateway = PaymentgatewayFactory.create_payment_gateway(arg.get('gateway'))
        customer_model = CustomersModel()
        customer = customer_model.find_one(self.session, arg)
        if customer:
            return customer
        data = gateway.createCustomer({
            'email': arg['email']
        })
        customer = customer_model.insert_one(self.session, {**arg, 'gateway_cust_id': data.get('id')})
        return customer
    
    def cancelSubscription(self, arg):
        subs = SubscriptionsModel().find_one(self.session, {'id': arg['sub_id']})
        gateway = PaymentgatewayFactory.create_payment_gateway(subs.get('gateway'))
        data = gateway.cancelSubscription(subs['gateway_sub_id'])
        updated_subs = SubscriptionsModel().update(self.session, {'id': arg['sub_id']}, {
            'cancel_at': data['cancel_at'] and datetime.fromtimestamp(data['cancel_at']) or data['cancel_at'],
            'canceled_at': data['canceled_at'] and datetime.fromtimestamp(data['canceled_at']) or data['canceled_at'],
            'cancel_at_period_end': data['cancel_at_period_end'],
            'status': 'ending'
        })
        return updated_subs