from flask import request
import json
from models.plans import PlansModel
from databases.postgres import Postgres
from facade.plans import PlanFacade
import jsonschema
import json

class PlanController:
    def __init__(self) -> None:
        self.__model = PlansModel()

    def index(self):
        with Postgres().session.begin() as session:
            data = PlanFacade(session).findAllPlans()
            return json.loads(json.dumps({'message': 'Plan List', 'data': data}, default=str)) 

    def create(self):
        schema = {
            "type": "object",
            "properties": {
                "currency": {"type": "string"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "gateway": {"type": "string"}
            },
            "required": ["currency", "name", "price", "gateway"]
        }
        try:
            jsonschema.validate(request.json, schema)
            print(request.json)
        except jsonschema.exceptions.ValidationError as e:
            return json.dumps({'error': e.message}), 400
        with Postgres().session.begin() as session:
            data = PlanFacade(session).createPlan(request.json)
            return json.loads(json.dumps({'message': 'Plan Created', 'data': data}, default=str))
