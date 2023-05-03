from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

# Create Flask application instance
app = Flask(__name__)

# Set MongoDB URI and database name in Flask app configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'
app.config['MONGO_DBNAME'] = 'db'

# Create PyMongo client and database instance
client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DBNAME']]

# Define User resource fields
user_fields = ['name', 'email', 'password']

# Define endpoint for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users)

# Define endpoint for getting a user by ID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

# Define endpoint for creating a new user
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    for field in user_fields:
        if field not in user_data:
            return jsonify({'error': f'Missing {field} field'}), 400
    user_id = db.users.insert_one(user_data).inserted_id
    return jsonify({'message': f'User created with ID: {str(user_id)}'}), 201

# Define endpoint for updating a user by ID
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    if not user_data:
        return jsonify({'error': 'No data provided to update'}), 400
    for field in user_fields:
        if field not in user_data:
            return jsonify({'error': f'Missing {field} field'}), 400
    result = db.users.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
    if result.modified_count > 0:
        return jsonify({'message': f'User with ID {user_id} updated'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Define endpoint for deleting a user by ID
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.users.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': f'User with ID {user_id} deleted'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
