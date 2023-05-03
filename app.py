from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['db']
collection = db['users']

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('email', type=str)
parser.add_argument('password', type=str)

class Users(Resource):
    def get(self):
        users = db.users.find()
        return list(users)

    def post(self):
        args = parser.parse_args()
        user_id = db.users.insert_one(args).inserted_id
        return {'id': str(user_id)}

class User(Resource):
    def get(self, user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user is not None:
            return user
        else:
            return {'error': 'User not found'}

    def put(self, user_id):
        args = parser.parse_args()
        db.users.update_one({'_id': ObjectId(user_id)}, {'$set': args})
        return {'id': user_id}

    def delete(self, user_id):
        db.users.delete_one({'_id': ObjectId(user_id)})
        return {'id': user_id
                
class UserTomorrow(Resource):
    def get(self, user_id, tomorrow):
        

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserTomorrow, '/users/<user_id>/<tomorrow>')

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)
