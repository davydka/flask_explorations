from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'unsecure_test'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create /auth

items = []

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='field is required'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': 'item exists'}, 400

        data = Items.parser.parse_args()
        item = {'name': data['name'], 'price': data['price']}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return { 'message': 'item deleted' }

    @jwt_required()
    def put(self, name):
        data = Items.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items))
        if item is None:
            item = {'name': data['name'], 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemsList(Resource):
    def get(sef):
        return {'items': items}

api.add_resource(Items, '/items/<string:name>')
api.add_resource(ItemsList, '/items')

app.run(port=5050, debug=True)
