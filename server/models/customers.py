from sqlalchemy import Table, Column, Integer, String, DECIMAL, DateTime, Boolean, Text, select, update
from databases.meta import Base

class CustomersModel():
    def __init__(self):
        self.Customer()
        self.columns = ['id', 'email', 'gateway', 'gateway_cust_id', 'description', 'name']

    def find_one(self, session, filter):
        statement = select(self.Customer).filter_by(**filter)
        user_obj = session.scalars(statement).first()
        return user_obj and user_obj.__dict__ or None

    def insert_one(self, session, data):
        customer = self.Customer(**{key: value for key, value in data.items() if key in self.columns})
        session.add(customer)
        user_obj =  session.scalars(
            select(self.Customer).filter_by(email=customer.email, gateway=customer.gateway)
        ).first()
        return user_obj and user_obj.__dict__ or None
    
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
        
        if updated_customer:
            return updated_customer.__dict__
        
        return None
    
    def delete(self, session, filter):
        data_to_delete = session.query(self.Customer).filter_by(**filter).all()

        if data_to_delete:
            # Delete the data
            for data in data_to_delete:
                session.delete(data)
            
            return True
        
        return True

    class Customer(Base):
        __tablename__ = 'customers'
        id = Column(Integer, primary_key=True)
        email = Column(String)
        gateway = Column(String)
        gateway_cust_id = Column(String, unique=True)
        description = Column(Text)
        name = Column(String)
    