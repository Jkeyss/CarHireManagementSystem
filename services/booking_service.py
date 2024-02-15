class BookingOperations:
    def __init__(self, booking_dao, vehicle_service):
        self.booking_dao = booking_dao
        self.vehicle_service = vehicle_service

    def validate_booking_duration(self, booking_data):
        date_hired = booking_data.get('date_hired')
        return_date = booking_data.get('return_date')

        if (return_date - date_hired).days > 7:
            raise ValueError("Booking duration cannot exceed 7 days")

    def validate_vehicle_availability(self, booking_data):
        vehicle_id = booking_data.get('vehicle_id')

        if not self.vehicle_service.check_availability(vehicle_id):
            raise ValueError("Vehicle is not available for booking")

    def create_booking(self, booking_data):
        self.validate_booking_duration(booking_data)
        self.validate_vehicle_availability(booking_data)
        return self.booking_dao.add(booking_data)

    def update_booking(self, booking_id, booking_data):
        self.validate_booking_duration(booking_data)
        self.validate_vehicle_availability(booking_data)
        return self.booking_dao.update(booking_id, booking_data)

    def delete_booking(self, booking_id):
        return self.booking_dao.delete(booking_id)