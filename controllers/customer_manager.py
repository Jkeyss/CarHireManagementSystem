from models.models import Customer


class CustomerManager:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def add_customer(self, customer_data):
        # Validate Input
        if not self._is_valid_customer_data(customer_data):
            raise ValueError("Invalid customer data")

        # Add Customer to Database
        customer = self.customer_dao.add(customer_data)
        return customer

    def update_customer(self, customer_id, customer_data):
        # Validate Input
        if not self._is_valid_customer_data(customer_data):
            raise ValueError("Invalid customer data")

        # Update Customer in Database
        customer = self.customer_dao.update(customer_id, customer_data)
        return customer

    def delete_customer(self, customer_id):
        # Make Sure Record Exists in Database
        if not self.get_customer(customer_id):
            raise ValueError("Customer does not exist")

        # Delete customer from Database
        self.customer_dao.delete(customer_id)

    def get_customer(self, customer_id):
        # Get Customer from Database
        return self.customer_dao.get(customer_id)

    # Utility -> Input Validation
    def _is_valid_customer_data(self, customer_data):
        if not isinstance(customer_data, dict):
            return False
        required_fields = {"first_name", "last_name", "email", "phone"}
        return all(field in customer_data for field in required_fields)
