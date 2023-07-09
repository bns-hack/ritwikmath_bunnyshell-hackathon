from sqlalchemy import Table, Column, Integer, String, DECIMAL, DateTime, Boolean, Text, select, update
from databases.meta import Base

class CustomersModel():
    def __init__(self):
        self.Customer()
        self.columns = ['id', 'email', 'gateway', 'gateway_cust_id', 'description', 'name']

    def find_one(self, session, filter):
        statement = select(self.Customer).filter_by(**filter)
        user_obj = session.scalars(statement).first()
        return user_obj.__dict__

    def insert_one(self, session, data):
        customer = self.Customer(**{key: value for key, value in data.items() if key in self.columns})
        session.add(customer)
        user_obj =  session.scalars(
            select(self.Customer).filter_by(email=customer.email, gateway=customer.gateway)
        ).first()
        return user_obj.__dict__
    
    def update(self, session, filter, data):
        statement = (
            update(self.Customer)
            .where(*[
                self.Customer.email == filter['email'],
                self.Customer.gateway == filter['gateway']
            ])
            .values(**data)
            .returning(self.Customer)
        )
        updated_customer = session.scalars(statement).first()
        print(updated_customer, end="\n\n\n\n")
        
        if updated_customer:
            return updated_customer.__dict__
        
        return None

    class Customer(Base):
        __tablename__ = 'customers'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        gateway = Column(String)
        gateway_cust_id = Column(String, unique=True)
        description = Column(Text)
        name = Column(String)
    