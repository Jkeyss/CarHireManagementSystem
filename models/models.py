
class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, model, make, year, registration_number, available):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.model = model
        self.make = make
        self.year = year
        self.registration_number = registration_number
        self.available = available


class Booking:
    def __init__(self, booking_id, customer_id, vehicle_id, date_hired, return_date, payment_status):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.date_hired = date_hired
        self.return_date = return_date
        self.payment_status = payment_status


class Invoice:
    def __init__(self, invoice_id, booking_id, total_amount, payment_date):
        self.invoice_id = invoice_id
        self.booking_id = booking_id
        self.total_amount = total_amount
        self.payment_date = payment_date