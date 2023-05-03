from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['db']
collection = db['users']

class User(Resource):
    def get(self, user_id=None):
        if user_id:
            user = collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
                return {"message": "User found", "data": user}, 200
            else:
                return {"message": "User not found"}, 404
        else:
            users = []
            for user in collection.find():
                user['_id'] = str(user['_id'])
                users.append(user)
            return {"message": "Users found", "data": users}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = {"name": args['name'], "email": args['email'], "password": args['password']}
        result = collection.insert_one(user)

        user['_id'] = str(result.inserted_id)
        return {"message": "User created", "data": user}, 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            updated_user = {}
            for field in ['name', 'email', 'password']:
                if args[field]:
                    updated_user[field] = args[field]
                else:
                    updated_user[field] = user[field]

            collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
            updated_user['_id'] = str(user_id)
            return {"message": "User updated", "data": updated_user}, 200
        else:
            return {"message": "User not found"}, 404

    def delete(self, user_id):
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return {"message": "User deleted"}, 204
        else:
            return {"message": "User not found"}, 404

api.add_resource(User, '/users', '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
