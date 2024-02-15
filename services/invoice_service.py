from datetime import datetime


class InvoiceService:
	def __init__(self, invoice_dao, booking_dao, booking_service):
		self.invoice_dao = invoice_dao
		self.booking_dao = booking_dao
		self.booking_service = booking_service

	def generate_invoice(self, booking_id):
		booking = self.booking_dao.get(booking_id)
		total_amount = calculate_total_amount(booking)

		invoice_data = {
			"booking_id": booking_id,
			"total_amount": total_amount,
			"payment_date": None
		}
		return self.invoice_dao.add(invoice_data)

	def handle_payment(self, invoice_id):
		invoice = self.invoice_dao.get(invoice_id)
		booking_id = invoice['booking_id']
		booking = self.booking_dao.get(booking_id)

		if invoice is None:
			raise ValueError("Invoice not found")

		if booking is None:
			raise ValueError("No booking corresponding to invoice was found")

		invoice['payment_date'] = datetime.now().date()
		booking['payment_status'] = 'PAID'
		self.booking_service.update_booking(booking_id, booking)
		return self.invoice_dao.update(invoice_id, invoice)


def calculate_total_amount(booking, daily_rate=200.75):
	# total amount = number of days * daily rate
	date_hired = booking.get('date_hired')
	return_date = booking.get('return_date')
	num_days = (return_date - date_hired).days
	return num_days * daily_rate
