from flask import Blueprint, request
import json
from controllers.customers import Customertroller

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login')
def login():
    return Customertroller().login()