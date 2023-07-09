from sqlalchemy import Table, Column, Integer, String, DECIMAL, DateTime, Boolean, ForeignKey, select
from databases.meta import Base

class SubscriptionsModel():
    def __init__(self):
        self.Subscription()
        self.columns = ['id', 'customer_id', 'gateway', 'gateway_sub_id', 'cancel_at', 'cancel_at_period_end', 'canceled_at', 'created_at', 'started_at', 'currency', 'current_period_start', 'current_period_end', 'status', 'amount', 'plan_id']

    def find(self, session, filter = {}):
        filter.update({})
        statement = select(self.Subscription).filter_by(**filter)
        subscriptions = [subscription.__dict__ for subscription in session.scalars(statement).all()]
        return subscriptions

    def find_one(self, session, filter):
        statement = select(self.Subscription).filter_by(**filter)
        subscription_obj = session.scalars(statement).first()
        return subscription_obj.__dict__

    def insert_one(self, session, data):
        subscription = self.Subscription(**{key: value for key, value in data.items() if key in self.columns})
        session.add(subscription)
        subscription_obj =  session.scalars(
            select(self.Subscription).filter_by(customer_id=subscription.customer_id, plan_id=subscription.plan_id)
        ).first()
        return subscription_obj.__dict__

    class Subscription(Base):
        __tablename__ = 'subscriptions'
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key=True)
        customer_id = Column(ForeignKey('customers.id'))
        gateway = Column(String)
        gateway_sub_id = Column(String, unique=True)
        cancel_at = Column(DateTime)
        cancel_at_period_end = Column(Boolean)
        canceled_at = Column(DateTime)
        created_at = Column(DateTime)
        started_at = Column(DateTime)
        currency = Column(String)
        current_period_start = Column(DateTime)
        current_period_end = Column(DateTime)
        status = Column(String)
        amount = Column(DECIMAL(10,2))
        plan_id = Column(ForeignKey('plans.id'))
    