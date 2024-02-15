from models.models import Customer
class CustomerManager:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def add_customer(self, customer_data):
        # new_customer = Customer(**customer_data)
        customer = self.customer_dao.add(customer_data)
        return customer

    def update_customer(self, customer_id, customer_data):
        self.customer_dao.update(customer_id, customer_data)

    def delete_customer(self, customer_id):
        self.customer_dao.delete(customer_id)

    def get_customer(self, customer_id):
        return self.customer_dao.get(customer_id)