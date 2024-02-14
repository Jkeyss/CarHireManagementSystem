from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
	return 'Hello World!'


# HTTP GET -> an endpoint to get customer
@app.route('/get-customer/<int:customer_id', methods=['GET'])
def get_customer(customer_id):
	pass


# HTTP PUT -> an endpoint to update customer
@app.route('/update-customer/<int:customer_id', methods=['PUT'])
def update_customer(customer_id):
	pass


# HTTP POST -> an endpoint to add new customer
@app.route('/add-customer', methods=['POST'])
def add_customer():
	pass


# HTTP DELETE -> an endpoint to delete customer
@app.route('/delete-customer/<int:customer_id', methods=['DELETE'])
def update_customer(customer_id):
	pass


if __name__ == '__main__':
	app.run()
