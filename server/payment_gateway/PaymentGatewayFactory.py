from payment_gateway.GatewayAbstract import GatewayAbstract as Gateway
from payment_gateway.stripe import Stripe

class PaymentgatewayFactory:
    @staticmethod
    def create_payment_gateway(name) -> Gateway:
        if name == 'stripe':
            return Stripe()