from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'unsecure_test'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create /auth

items = []

class Items(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'item exists'}, 400

        data = request.get_json()
        item = {'name': data['name'], 'price': data['price']}
        items.append(item)
        return item, 201

class ItemsList(Resource):
    def get(sef):
        return {'items': items}

api.add_resource(Items, '/items/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5050, debug=True)
