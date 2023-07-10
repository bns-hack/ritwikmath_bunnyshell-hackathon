from abc import ABC, abstractmethod

class GatewayAbstract(ABC):
    @abstractmethod
    def getSubscriptions(self, filter):
        pass

    @abstractmethod
    def getSubscription(self, sub_id):
        pass

    @abstractmethod
    def createSubscription(self, data):
        pass

    @abstractmethod
    def createCustomer(self, customer):
        pass

    @abstractmethod
    def deleteCustomer(self, cust_id):
        pass

    @abstractmethod
    def getCards(self, cust_id):
        pass

    @abstractmethod
    def createPlan(self, data):
        pass

    @abstractmethod
    def createProduct(self, data):
        pass

    @abstractmethod
    def createSetupIntent(self, cust_id):
        pass

    @abstractmethod
    def cancelSubscription(self, sub_id):
        pass