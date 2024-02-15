from datetime import datetime


class BookingServices:
	"""
	A service to handle booking logic that then routes the data to
	the Booking DAO to perform CRUD operations.
	"""

	def __init__(self, booking_dao, vehicle_service):
		self.booking_dao = booking_dao
		self.vehicle_service = vehicle_service

	def create_booking(self, booking_data):
		"""
		Validates booking data then sends it to the booking DAO to add
		to the database.

		Parameters
		----------
		booking_data : dict
			A dictionary containing the booking data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			inserted into the database.
		"""
		self.run_all_validation(booking_data)
		return self.booking_dao.add(booking_data)

	def update_booking(self, booking_id, booking_data):
		"""
		Validates input then sends it to the booking DAO to update the
		booking record with booking_id.

		Parameters
		----------
		booking_id : int
			The booking's id
		booking_data : dict
			A dictionary containing the booking data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			updated in the database.
		"""
		self.run_all_validation(booking_data)
		if not self.booking_dao.get(booking_id):
			raise ValueError("Booking does not exist")
		return self.booking_dao.update(booking_id, booking_data)

	def delete_booking(self, booking_id):
		"""
		Validates input then sends it to the booking DAO to delete the
		booking with booking_id.

		Parameters
		----------
		booking_id : int
			The booking id
		"""
		if not self.booking_dao.get(booking_id):
			raise ValueError("Booking does not exist")
		return self.booking_dao.delete(booking_id)

	def get_booking(self, booking_id):
		"""
		Gets booking record from database if the booking_id is invalid it will return None.

		Parameters
		----------
		booking_id : int
			The records booking_id

		Returns
		-------
		dict
			A dictionary containing the data from the record that was retrieved
			from the database.
		"""
		if not self.booking_dao.get(booking_id):
			raise ValueError("Booking does not exist")
		return self.booking_dao.get(booking_id)

	def run_all_validation(self, booking_data):
		"""
		Checks booking duration to make sure it does not exceed 7 days
		and the booking is not more than 7 days in advance. This then
		makes sure the requested vehicle is available in the given time
		frame and validates required fields.

		Parameters
		----------
		booking_data : dict
			The booking record.
		"""
		self._validate_booking_duration(booking_data)
		self._validate_vehicle_availability(booking_data)
		if not self._validate_booking_fields(booking_data):
			raise ValueError("Required booking fields are missing")

	def _validate_booking_duration(self, booking_data):
		date_hired = booking_data.get('date_hired')
		return_date = booking_data.get('return_date')

		if (return_date - date_hired).days > 7:
			raise ValueError("Booking duration cannot exceed 7 days")
		elif (date_hired - datetime.now().date()).days > 7:
			raise ValueError("Booking cannot be made more than 7 days in advance")

	def _validate_vehicle_availability(self, booking_data):
		vehicle_id = booking_data.get('vehicle_id')
		date_hired = booking_data.get('date_hired')
		return_date = booking_data.get('return_date')

		if self.vehicle_service.get_vehicle(vehicle_id) is None:
			return ValueError("A vehicle with that vehicle_id does not exist")
		elif not self.booking_dao.is_vehicle_available(vehicle_id, start_date=date_hired, end_date=return_date):
			raise ValueError("Vehicle is not available for booking during that time frame")

	def _validate_booking_fields(self, booking_data):
		if not isinstance(booking_data, dict):
			return False
		required_fields = {"customer_id", "vehicle_id", "date_hired", "return_date", "payment_status"}
		return all(field in booking_data for field in required_fields)

	def generate_daily_report(self):
		return self.booking_dao.get_daily_bookings()

	def send_confirmation_email(self):
		pass
