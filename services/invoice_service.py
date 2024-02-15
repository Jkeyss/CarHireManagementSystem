from datetime import datetime


class InvoiceService:
	def __init__(self, invoice_dao, booking_dao, booking_service):
		self.invoice_dao = invoice_dao
		self.booking_dao = booking_dao
		self.booking_service = booking_service

	def generate_invoice(self, booking_id):
		"""
		Creates a new invoice and links it to the booking_id.

		Parameters
		----------
		booking_id : int
			The booking linked to the invoice.

		Returns
		-------
		dict
			A dictionary containing the data from the invoice that was added
			to the database.
		"""
		booking = self.booking_dao.get(booking_id)
		if not booking:
			raise ValueError("Invalid booking_id")

		total_amount = calculate_total_amount(booking)
		invoice_data = {
			"booking_id": booking_id,
			"total_amount": total_amount,
			"payment_date": None
		}
		return self.invoice_dao.add(invoice_data)

	def update_invoice(self, invoice_id, invoice):
		"""
		Validates input then sends data to the invoice DAO to update the
		record with invoice_id in the database.

		Parameters
		----------
		invoice_id : int
			The invoice's id
		invoice : dict
			A dictionary containing the invoice data.

		Returns
		-------
		dict
			A dictionary containing the data from the record that was just
			updated in the database.
		"""
		if not self._validate_invoice_fields(invoice):
			raise ValueError("Invalid invoice data")
		if not self.invoice_dao.get(invoice_id):
			raise ValueError("Invalid invoice_id")
		return self.invoice_dao.update(invoice_id, invoice)

	def get_invoice(self, invoice_id):
		"""
		Gets the invoice from database. If the invoice_id is invalid it will return None.

		Parameters
		----------
		invoice_id : int
			The invoice's id

		Returns
		-------
		dict
			A dictionary containing the data from the record that was retrieved
			from the database.
		"""
		if not self.invoice_dao.get(invoice_id):
			raise ValueError("Invoice does not exist")
		return self.invoice_dao.get(invoice_id)

	def delete_invoice(self, invoice_id):
		"""
		Calls the invoice DAO to delete the invoice record.

		Parameters
		----------
		invoice_id : int
			The invoice's id
		"""
		return self.invoice_dao.delete(invoice_id)

	def handle_payment(self, invoice_id):
		"""
		Handles payment of the invoice by including a payment_date to
		the invoice, then marks the booking payment_status field as PAID.
		Finally, it updates the records in the database to reflect this.

		Parameters
		----------
		invoice_id : int
			The invoice's id.

		Returns
		-------
		dict
			A dictionary containing the data from the invoice that was
			updated in the database.
		"""
		invoice = self.invoice_dao.get(invoice_id)
		booking_id = invoice['booking_id']
		booking = self.booking_dao.get(booking_id)

		if invoice is None:
			raise ValueError("Invoice not found")

		if booking is None:
			raise ValueError("No booking with that invoice_id was found")

		invoice['payment_date'] = datetime.now().date()
		booking['payment_status'] = 'PAID'
		self.booking_service.update_booking(booking_id, booking)
		return self.update_invoice(invoice_id, invoice)

	def _validate_invoice_fields(self, invoice_data):
		"""
		Validates the input to make sure all required fields are included.

		Parameters
		----------
		invoice_data : dict
			A dictionary containing the vehicle data.

		Returns
		-------
		bool
			True if the required data is included, otherwise False.
		"""
		if not isinstance(invoice_data, dict):
			return False
		required_fields = {"booking_id", "total_amount", "payment_date"}
		return all(field in invoice_data for field in required_fields)


def calculate_total_amount(booking, daily_rate=200.75):
	# total amount = number of days * daily rate
	date_hired = booking.get('date_hired')
	return_date = booking.get('return_date')
	num_days = (return_date - date_hired).days
	return num_days * daily_rate
