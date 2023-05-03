# Flask CRUD Application with MongoDB

This is a Flask application that performs CRUD (Create, Read, Update, Delete) operations on a MongoDB database for a User resource using a REST API.

## Requirements

- Python 3.x
- Flask
- PyMongo
- Postman (for testing)

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/adarsh217/FlaskCRUD.git
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a new MongoDB database and collection for the application.

5. Set the MongoDB URI and database name in the Flask application configuration by modifying the `config.py` file:

   ```
   MONGO_URI = 'mongodb://localhost:27017/db'
   MONGO_DBNAME = 'db'
   ```

## Usage

1. Start the Flask application:

   ```
   flask run
   ```

2. Using Postman, create new HTTP requests for each of the REST API endpoints:

   ```
   GET /users - Returns a list of all users.
   GET /users/<id> - Returns the user with the specified ID.
   POST /users - Creates a new user with the specified data.
   PUT /users/<id> - Updates the user with the specified ID with the new data.
   DELETE /users/<id> - Deletes the user with the specified ID.
   ```

3. Send requests to the endpoints to test the CRUD operations on the User resource.

4. Verify that the responses are correct and the database is being updated correctly.
