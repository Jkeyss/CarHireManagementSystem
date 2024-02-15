from models.models import Customer


class CustomerManager:
	"""
	A controller to handle input validation that then routes the data to
	the Customer DAO to perform CRUD operations.
	"""

	def __init__(self, customer_dao):
		self.customer_dao = customer_dao

	def add_customer(self, customer_data):
		"""
		Validates customer data then sends it to the customer DAO to add
		to the database.

		Parameters
		----------
		customer_data : dict
			A dictionary containing the customer data.

		Returns
		-------
		dict
			A dictionary containing the data from the row that was just
			inserted into the database.
		"""
		if not self._is_valid_customer_data(customer_data):
			raise ValueError("Invalid customer data")

		# Add Customer to Database
		customer = self.customer_dao.add(customer_data)
		return customer

	def update_customer(self, customer_id, customer_data):
		"""
		Validates input then sends it to the customer DAO to update the
		customer with customer_id in the database.

		Parameters
		----------
		customer_id : int
			The customer's id
		customer_data : dict
			A dictionary containing the customer data.

		Returns
		-------
		dict
			A dictionary containing the data from the row that was just
			updated in the database.
		"""
		if not self._is_valid_customer_data(customer_data):
			raise ValueError("Invalid customer data")

		# Update Customer in Database
		customer = self.customer_dao.update(customer_id, customer_data)
		return customer

	def delete_customer(self, customer_id):
		"""
		Validates input then sends it to the customer DAO to delete the
		customer with customer_id.

		Parameters
		----------
		customer_id : int
			The customer's id
		"""
		if not self.get_customer(customer_id):
			raise ValueError("Customer does not exist")

		# Delete customer from database
		self.customer_dao.delete(customer_id)

	def get_customer(self, customer_id):
		"""
		Gets customer from database if the customer_id is invalid it will return None.

		Parameters
		----------
		customer_id : int
			The customer's id

		Returns
		-------
		dict
			A dictionary containing the data from the row that was retrieved
			from the database.
		"""
		return self.customer_dao.get(customer_id)

	def _is_valid_customer_data(self, customer_data):
		"""
		Validates the input to make sure all required fields are included.

		Parameters
		----------
		customer_data : dict
			A dictionary containing the customer data.

		Returns
		-------
		bool
			True if the required data is included, otherwise False.
		"""
		if not isinstance(customer_data, dict):
			return False
		required_fields = {"first_name", "last_name", "email", "phone"}
		return all(field in customer_data for field in required_fields)
