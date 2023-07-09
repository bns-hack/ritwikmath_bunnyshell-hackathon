from sqlalchemy import Table, Column, Integer, String, DECIMAL, DateTime, Boolean, select
from databases.meta import Base

class PlansModel():
    def __init__(self):
        self.Plan()
        self.columns = ['id', 'name', 'group_plans', 'gateway', 'gateway_product_id', 'gateway_price_id', 'price', 'currency', 'recurring_plan']

    def find(self, session, filter = {}):
        filter.update({})
        statement = select(self.Plan).filter_by(**filter)
        plans = [plan.__dict__ for plan in session.scalars(statement).all()]
        return plans

    def find_one(self, session, filter):
        statement = select(self.Plan).filter_by(**filter)
        plan_obj = session.scalars(statement).first()
        return plan_obj.__dict__

    def insert_one(self, session, data):
        plan = self.Plan(**{key: value for key, value in data.items() if key in self.columns})
        session.add(plan)
        plan_obj =  session.scalars(
            select(self.Plan).filter_by(gateway_price_id=plan.gateway_price_id)
        ).first()
        return plan_obj.__dict__

    class Plan(Base):
        __tablename__ = 'plans'
        __table_args__ = {'extend_existing': True}
        id = Column(Integer, primary_key=True)
        name = Column(String)
        group_plans = Column(String)
        gateway = Column(String)
        gateway_product_id = Column(String, unique=True)
        gateway_price_id = Column(String, unique=True)
        price = Column(DECIMAL(10,2))
        currency = Column(String)
        recurring_plan = Column(Boolean)
    