from payment_gateway.GatewayAbstract import GatewayAbstract as Gateway
import stripe

class Stripe(Gateway):
    def __init__(self):
        print('Stripe gateway initializing')

    def getSubscriptions(self, filter):
        return stripe.Subscription.list(**filter).to_dict_recursive()

    def getSubscription(self, sub_id):
        return stripe.Subscription.retrieve(sub_id).to_dict_recursive()

    def createSubscription(self, data):
        return stripe.Subscription.create(**data).to_dict_recursive()

    def createCustomer(self, customer):
        return stripe.Customer.create(**customer).to_dict_recursive()
    
    def deleteCustomer(self, cust_id):
        return stripe.Customer.delete(cust_id).to_dict_recursive()

    def getCards(self, cust_id):
        return stripe.PaymentMethod.list(customer=cust_id).to_dict_recursive()

    def createPlan(self, data):
        return stripe.Price.create(**data).to_dict_recursive()

    def createProduct(self, data):
        return stripe.Product.create(**data).to_dict_recursive()

    def createSetupIntent(self, cust_id):
        return stripe.SetupIntent.create(customer = cust_id).to_dict_recursive()
    
    def cancelSubscription(self, sub_id):
        return stripe.Subscription.modify(sub_id, cancel_at_period_end = True).to_dict_recursive()
