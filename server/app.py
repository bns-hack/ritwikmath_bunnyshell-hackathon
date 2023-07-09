import os
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app: Flask = Flask(__name__)

from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from databases.postgres import Postgres
from databases.meta import Base
from models.subscriptions import SubscriptionsModel
from models.plans import PlansModel
from models.customers import CustomersModel
from middlewares.auth import AuthMiddleware
import stripe
import os

app: Flask = Flask(__name__)
stripe.api_key = os.getenv('STRIPE_API_KEY')
Postgres().createEngine().createConnection()
SubscriptionsModel()
PlansModel()
CustomersModel()
Base.metadata.create_all(Postgres().engine)
app.wsgi_app = AuthMiddleware(app.wsgi_app)