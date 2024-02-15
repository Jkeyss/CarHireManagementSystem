
class BaseDAO:
    def __init__(self, db_manager, table_name, id_name):
        self.db_manager = db_manager
        self.table_name = table_name
        self.id_name = id_name


    def add(self, data):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql, list(data.values()))
        conn.commit()
        # Get the ID of the last inserted row
        record_id = cursor.lastrowid
        # Fetch the newly inserted object from the database
        record = self.get(record_id)
        cursor.close()
        return record

    def update(self, identifier, data):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.id_name} = %s"
        cursor.execute(sql, list(data.values()) + [identifier])
        conn.commit()
        record = self.get(identifier)
        cursor.close()
        return record

    def delete(self, identifier):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        sql = f"DELETE FROM {self.table_name} WHERE {self.id_name} = %s"
        cursor.execute(sql, (identifier,))
        conn.commit()
        cursor.close()

    def get(self, identifier):
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        sql = f"SELECT * FROM {self.table_name} WHERE {self.id_name} = %s"
        cursor.execute(sql, (identifier,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return self.row_to_dict(row, cursor.description)
        return None

    # UTILITY METHOD --> Turn Fetched Rows into Dictionary
    def row_to_dict(self, row, column_descriptions):
        dictionary = {}
        for column, value in zip(column_descriptions, row):
            dictionary[column[0]] = value
        return dictionary


class CustomerDAO(BaseDAO):
    def __init__(self, db_manager):
        super().__init__(db_manager, "Customer", "customer_id")


class VehicleDAO(BaseDAO):
    def __init__(self, db_manager):
        super().__init__(db_manager, "Vehicle", "vehicle_id")


class BookingDAO(BaseDAO):
    def __init__(self, db_manager):
        super().__init__(db_manager, "Booking", "booking_id")


class InvoiceDAO(BaseDAO):
    def __init__(self, db_manager):
        super().__init__(db_manager, "Invoice", "invoice_id")