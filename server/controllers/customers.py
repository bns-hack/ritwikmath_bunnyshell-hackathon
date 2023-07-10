from flask import request
import json
from models.customers import CustomersModel
from databases.postgres import Postgres
from facade.customers import CustomerFacade
from payment_gateway.PaymentGatewayFactory import PaymentgatewayFactory
import json
import jsonschema

class Customertroller:
    def __init__(self) -> None:
        self.__model = CustomersModel()

    def me(self):
        with Postgres().session.begin() as session:
            data = CustomersModel().find_one(session, {
                'email': request.environ['loggedin_user'].get('email')
            })
            return json.loads(json.dumps({'message': 'Loggedin customer', 'data': data}, default=str))

    def create(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "country": {"type": "string"},
                "gateway": {"type": "string"}
            },
            "required": ["name", "country", "gateway"]
        }
        try:
            jsonschema.validate(request.json, schema)
            print(request.json)
        except jsonschema.exceptions.ValidationError as e:
            return json.dumps({'error': e.message}), 400
        with Postgres().session.begin() as session:
            request.json['email'] = request.environ['loggedin_user'].get('email')
            data = CustomerFacade(session).createCustomer(request.json)
            return json.loads(json.dumps({'message': 'Customer Created', 'data': data}, default=str))
        
    def destroy(self):
        with Postgres().session.begin() as session:
            data = CustomerFacade(session).deleteCustomer({'email': request.environ['loggedin_user'].get('email')})
            return json.loads(json.dumps({'message': 'Customer delete successful', 'data': data}, default=str))
    
    def setup_intent(self):
        with Postgres().session.begin() as session:
            data = CustomersModel().find_one(session, {
                'email': request.environ['loggedin_user'].get('email')
            })
            gateway = PaymentgatewayFactory.create_payment_gateway(data['gateway'])
            data = gateway.createSetupIntent(data['gateway_cust_id'])
            return json.loads(json.dumps({'message': 'Customer delete successful', 'data': data}, default=str))
