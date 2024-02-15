from datetime import datetime
from services.base_service import BaseService


class InvoiceService(BaseService):
	def __init__(self, invoice_dao, booking_dao, booking_service):
		required_fields = {
			"booking_id",
			"total_amount",
			"payment_date"
		}
		super().__init__(invoice_dao, required_fields)
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
		return self.dao.add(invoice_data)

	def update_invoice(self, invoice_id, invoice):
		"""
		Validates input then sends data to the invoice DAO to update the
		record with invoice_id

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
		super().update_record(invoice_id, invoice)

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
		super().get_record(invoice_id)

	def delete_invoice(self, invoice_id):
		"""
		Calls the invoice DAO to delete the invoice record.

		Parameters
		----------
		invoice_id : int
			The invoice's id
		"""
		super().delete_record(invoice_id)


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
		invoice = self.dao.get(invoice_id)
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


def calculate_total_amount(booking, daily_rate=200.75):
	# total amount = number of days * daily rate
	date_hired = booking.get('date_hired')
	return_date = booking.get('return_date')
	num_days = (return_date - date_hired).days
	return num_days * daily_rate
