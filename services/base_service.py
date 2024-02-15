class BaseService:
	def __init__(self, dao, required_fields):
		self.dao = dao
		self.required_fields = required_fields

	def create_record(self, data):
		"""
		Validates data then sends it to the DAO to add
		to the database.

		Parameters
		----------
		data : dict
			A dictionary containing the data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			inserted into the database.
		"""
		if not self._is_valid_data(data):
			raise ValueError("Invalid data")
		return self.dao.add(data)


	def update_record(self, record_id, data):
		"""
		Validates input then sends it to the relevant DAO to update the
		data record with the corresponding id.

		Parameters
		----------
		record_id : int
			The record's id
		data : dict
			A dictionary containing the record data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			updated in the database.
		"""
		if not self._is_valid_data(data):
			raise ValueError("Invalid data")
		if not self.dao.get(record_id):
			raise ValueError("Record does not exist")
		return self.dao.update(record_id, data)

	def delete_record(self, record_id):
		"""
		Validates input then sends it to the relevant DAO to delete the
		record with record_id.

		Parameters
		----------
		record_id : int
			The record_id
		"""
		if not self.dao.get(record_id):
			raise ValueError("Record does not exist")
		return self.dao.delete(record_id)

	def get_record(self, record_id):
		"""
		Gets record from database if the record_id is invalid it will return None.

		Parameters
		----------
		record_id : int
			The records id.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was retrieved
			from the database.
		"""
		if not self.dao.get(record_id):
			raise ValueError("Record does not exist")
		return self.dao.get(record_id)


	def _is_valid_data(self, data):
		"""
		Validates the input to make sure all required fields are included.

		Parameters
		----------
		data : dict
			A dictionary containing the customer data.

		Returns
		-------
		bool
			True if the required data is included, otherwise False.
		"""
		if not isinstance(data, dict):
			return False
		return all(field in data for field in self.required_fields)