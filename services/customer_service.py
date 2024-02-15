from services.base_service import BaseService


class CustomerService(BaseService):
	"""
	A service to handle customer logic that then routes the data to
	the Customer DAO to perform CRUD operations.
	"""

	def __init__(self, customer_dao):
		required_fields = {
			"first_name",
			"last_name",
			"email",
			"phone"
		}
		super().__init__(customer_dao, required_fields)

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
			A dictionary containing the data from the record that was just
			inserted into the database.
		"""
		# Add Customer to Database
		return super().create_record(customer_data)

	def update_customer(self, customer_id, customer_data):
		"""
		Validates input then sends it to the customer DAO to update the
		customer with customer_id.

		Parameters
		----------
		customer_id : int
			The customer's id
		customer_data : dict
			A dictionary containing the customer data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			updated in the database.
		"""
		return super().update_record(customer_id, customer_data)

	def delete_customer(self, customer_id):
		"""
		Validates input then sends it to the customer DAO to delete the
		customer with customer_id.

		Parameters
		----------
		customer_id : int
			The customer's id
		"""
		return super().delete_record(customer_id)

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
			A dictionary containing the data from the record that was retrieved
			from the database.
		"""
		return super().get_record(customer_id)
