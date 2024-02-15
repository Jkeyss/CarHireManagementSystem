from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from database.db import DatabaseManager
from models.daos import CustomerDAO
from controllers.customer_manager import CustomerManager
from decouple import Config, RepositoryEnv

app = Flask(__name__)

# Connect to database
DOTENV_FILE = './envs.env'
config = Config(RepositoryEnv(DOTENV_FILE))
mysql_config = {
	'host': config('DB_HOST'),
	'user': config('DB_USER'),
	'password': config('DB_PASSWORD'),
	'database': config('DB_DATABASE')
}
db_manager = DatabaseManager(**mysql_config)
db_manager.connect()
db_manager.create_tables()

# Create DAOs and Managers
customer_dao = CustomerDAO(db_manager)
customer_manager = CustomerManager(customer_dao)


@app.route('/')
def hello_world():
	return 'Hello World!'


# HTTP GET -> an endpoint to get customer
@app.route('/get-customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
	try:
		customer = customer_manager.get_customer(customer_id)
		return jsonify(customer=customer), 200
	except HTTPException as error:
		error.description = f"Customer with id: {customer_id} was not found in the database"
		return jsonify(error={error.name: error.description}), error.code


# HTTP PUT -> an endpoint to update customer
@app.route('/update-customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
	customer_data = request.json
	try:
		customer = customer_manager.update_customer(customer_id, customer_data)
		return jsonify(updated_customer=customer), 200
	except HTTPException as error:
		error.description = f"The Customer with {customer_id} could not be updated"
		return jsonify(error={error.name: error.description}), error.code


# HTTP POST -> an endpoint to add new customer
@app.route('/add-customer', methods=['POST'])
def add_customer():
	customer_data = request.json
	try:
		customer = customer_manager.add_customer(customer_data)
		return jsonify(customer=customer), 200
	except HTTPException as error:
		error.description = f"The Customer could not be added to the database"
		return jsonify(error={error.name: error.description}), error.code


# HTTP DELETE -> an endpoint to delete customer
@app.route('/delete-customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
	try:
		customer_manager.delete_customer(customer_id)
		return jsonify(success='success'), 200
	except HTTPException as error:
		error.description = f"Customer with id: {customer_id} could not be deleted"
		return jsonify(error={error.name: error.description}), error.code


if __name__ == '__main__':
	app.run(debug=True)
