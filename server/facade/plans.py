from payment_gateway.PaymentGatewayFactory import PaymentgatewayFactory
from models.plans import PlansModel

class PlanFacade:
    def __init__(self, session) -> None:
        self.session = session

    def findAllPlans(self):
        plans = PlansModel().find(self.session)
        return plans

    def createPlan(self, json):
        plans = []
        for gateway_name in json.get('gateway').split(","):
            gateway = PaymentgatewayFactory.create_payment_gateway(gateway_name)
            product_gateway = gateway.createProduct({
                'name': json.get('name')
            })
            plan_gateway = gateway.createPlan({
                'product': product_gateway['id'],
                'unit_amount': int(json.get('price'))*100,
                'currency': json.get('currency').lower(),
                'recurring': {'interval': 'month', 'interval_count': 1}
            })
            plan = PlansModel().insert_one(self.session, {
                'name': json.get('name'),
                'group_plans': json.get('group_plans'),
                'gateway': json.get('gateway'),
                'gateway_product_id': plan_gateway.get('product'),
                'gateway_price_id': plan_gateway.get('id'),
                'price': float(plan_gateway.get('unit_amount'))/100,
                'currency': json.get('currency'),
                'recurring_plan': json.get('recurring_plan'),
            })
            plans.append(plan)
        return plans