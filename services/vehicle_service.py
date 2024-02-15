from services.base_service import BaseService


class VehicleService(BaseService):
	def __init__(self, vehicle_dao):
		required_fields = {
			"type",
			"model",
			"make",
			"year",
			"registration_number",
			"available"
		}
		super().__init__(vehicle_dao, required_fields)

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
		return super().create_record(vehicle_data)

	def update_vehicle(self, vehicle_id, vehicle_data):
		"""
		Validates input then sends it to the vehicle DAO to update the
		vehicle with vehicle_id.

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
		return super().update_record(vehicle_id, vehicle_data)

	def delete_vehicle(self, vehicle_id):
		"""
		Validates input then sends it to the vehicle DAO to delete the
		vehicle with vehicle_id.

		Parameters
		----------
		vehicle_id : int
			The vehicle's id
		"""
		return super().delete_record(vehicle_id)

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
		return super().get_record(vehicle_id)
