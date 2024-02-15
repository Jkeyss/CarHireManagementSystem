class VehicleService:
	def __init__(self, vehicle_dao):
		self.vehicle_dao = vehicle_dao

	def add_vehicle(self, vehicle_data):
		"""
		Validates vehicle data then sends it to the vehicle DAO to add
		to the database.

		Parameters
		----------
		vehicle_data : dict
			A dictionary containing the vehicle data.

		Returns
		-------
		dict
			A dictionary containing the data from the row that was just
			inserted into the database.
		"""
		if not self._is_valid_vehicle_data(vehicle_data):
			raise ValueError("Invalid vehicle data")
		return self.vehicle_dao.add(vehicle_data)

	def get_vehicle(self, vehicle_id):
		"""
		Gets vehicle from database if the vehicle_id is invalid it will return None.

		Parameters
		----------
		vehicle_id : int
			The vehicle's id

		Returns
		-------
		dict
			A dictionary containing the data from the row that was retrieved
			from the database.
		"""
		if not self.vehicle_dao.get(vehicle_id):
			raise ValueError("Invoice does not exist")
		return self.vehicle_dao.get(vehicle_id)

	def update_vehicle(self, vehicle_id, vehicle_data):
		"""
		Validates input then sends it to the vehicle DAO to update the
		vehicle with vehicle_id in the database.

		Parameters
		----------
		vehicle_id : int
			The vehicle's id
		vehicle_data : dict
			A dictionary containing the vehicle data.

		Returns
		-------
		dict
			A dictionary containing the data from the row that was
			updated in the database.
		"""
		if not self._is_valid_vehicle_data(vehicle_data):
			raise ValueError("Invalid vehicle data")
		return self.vehicle_dao.update(vehicle_id, vehicle_data)

	def delete_vehicle(self, vehicle_id):
		"""
		Validates input then sends it to the vehicle DAO to delete the
		vehicle with vehicle_id.

		Parameters
		----------
		vehicle_id : int
			The vehicle's id
		"""
		if not self.get_vehicle(vehicle_id):
			raise ValueError("Vehicle does not exist")
		return self.vehicle_dao.delete(vehicle_id)

	def _is_valid_vehicle_data(self, vehicle_data):
		"""
		Validates the input to make sure all required fields are included.

		Parameters
		----------
		vehicle_data : dict
			A dictionary containing the vehicle data.

		Returns
		-------
		bool
			True if the required data is included, otherwise False.
		"""
		if not isinstance(vehicle_data, dict):
			return False
		required_fields = {"type", "model", "make", "year", "registration_number", "available"}
		return all(field in vehicle_data for field in required_fields)
