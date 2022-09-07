from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema,  whiskies_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/whiskies', methods= ['POST'])
@token_required
def create_whiskey(current_user_token):
    brand = request.json['brand']
    name = request.json['name']
    category = request.json['category']
    rating = request.json['rating']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(brand, name, category, rating, user_token = user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)
@api.route('/whiskies', methods = ['GET'])
@token_required
def get_whiskies(current_user_token):
    a_user = current_user_token.token
    whiskies = Whiskey.query.filter_by(user_token = a_user).all()
    response = whiskies_schema.dump(whiskies)
    return jsonify(response)

@api.route('/whiskies/<id>', methods = ['GET'])
@token_required
def get_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskies/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.brand = request.json['brand']
    whiskey.name = request.json['name']
    whiskey.category = request.json['category']
    whiskey.rating = request.json['rating']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskies/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)
