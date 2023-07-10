from payment_gateway.PaymentGatewayFactory import PaymentgatewayFactory
from models.customers import CustomersModel
from models.subscriptions import SubscriptionsModel

class CustomerFacade:
    def __init__(self, session) -> None:
        self.session = session

    def createCustomer(self, json):
        customers = []
        for gateway_name in json.get('gateway').split(","):
            gateway = PaymentgatewayFactory.create_payment_gateway(gateway_name)
            customer_gateway = gateway.createCustomer({
                'email': json['email'],
                'name': json['name'],
                'shipping': {
                    'name': json['name'],
                    'address': {
                        'country': json['country']
                    }
                }
            })
            customer = CustomersModel().insert_one(self.session, {
                'email': json.get('email'),
                'name': json.get('name'),
                'country': json.get('country'),
                'gateway': gateway_name,
                'gateway_cust_id': customer_gateway.get('id'),
                'description': json['country']
            })
            customers.append(customer)
        return customers

    def deleteCustomer(self, json):
        data = CustomersModel().find_one(self.session, {
            'email': json.get('email')
        })
        response = None
        if data:
            gateway = PaymentgatewayFactory.create_payment_gateway(data['gateway'])
            SubscriptionsModel().delete(self.session, {
                'customer_id': data['id']
            })
            CustomersModel().delete(self.session, {
                'email': json.get('email')
            })
            if data['gateway_cust_id']:
                try:
                    response = gateway.deleteCustomer(data['gateway_cust_id'])
                except:
                    pass
        return response
