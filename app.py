from flask import Flask, jsonify

app = Flask(__name__)

stores = [
    {
        'name': 'super store',
        'items': [
            {
                'name': 'super item',
                'price': 15.99
            }
        ]
    }
]

@app.route('/store', methods=['POST'])
def create_store():
    pass

@app.route('/store/<string:name>')
def get_store(name):
    pass

@app.route('/stores')
def get_stores():
    return jsonify({'stores': stores})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass

app.run(port=5050)
