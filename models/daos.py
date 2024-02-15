class BaseDAO:
	"""
	A base DAO class to be called by the child DAO's. The relevant
	CRUD operations will be handled dynamically by the child DAO
	injecting its manager class, table name and id name on
	initialization.
	"""

	def __init__(self, db_manager, table_name, id_name):
		self.db_manager = db_manager
		self.table_name = table_name
		self.id_name = id_name

	def add(self, data):
		"""
		Inserts record into database and returns the newly inserted record.

		Parameters
		----------
		data : dict
			A dictionary containing the record data.

		Returns
		-------
		dict
			A dictionary containing the record that was just inserted into
			the database.
		"""
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
		"""
		Updates existing record in database and returns the newly updated record.

		Parameters
		----------
		identifier : int
			Primary key id for record.
		data : dict
			A dictionary containing the record data.

		Returns
		-------
		dict
			A dictionary containing the record that was just updated in
			the database.
		"""
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
		"""
		Deletes existing record from database.

		Parameters
		----------
		identifier : int
			Primary key id for record.
		"""
		conn = self.db_manager.get_connection()
		cursor = conn.cursor()
		sql = f"DELETE FROM {self.table_name} WHERE {self.id_name} = %s"
		cursor.execute(sql, (identifier,))
		conn.commit()
		cursor.close()

	def get(self, identifier):
		"""
		Retrieves existing record in database.

		Parameters
		----------
		identifier : int
			Primary key id for record.

		Returns
		-------
		dict
			A dictionary containing the record that was just retrieved from
			the database.
		"""
		conn = self.db_manager.get_connection()
		cursor = conn.cursor()
		sql = f"SELECT * FROM {self.table_name} WHERE {self.id_name} = %s"
		cursor.execute(sql, (identifier,))
		row = cursor.fetchone()
		cursor.close()
		if row:
			return self.row_to_dict(row, cursor.description)
		return None

	def row_to_dict(self, row, column_descriptions):
		"""
		Utility method to create dict from database row.

		Parameters
		----------
		row : list
			A database row fetched from the cursor.
		column_descriptions : list
			Descriptions of the columns obtained from the cursor

		Returns
		-------
		dict
			A dictionary containing the row data.
		"""
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

	def is_vehicle_available(self, vehicle_id, start_date, end_date):
		conn = self.db_manager.get_connection()
		cursor = conn.cursor()

		sql = """
		    SELECT COUNT(*)
		    FROM Booking
		    WHERE vehicle_id = %s
		    AND return_date > %s
		    AND date_hired < %s
		"""
		cursor.execute(sql, (vehicle_id, start_date, end_date))
		count = cursor.fetchone()[0]

		cursor.close()
		conn.close()

		return count == 0

	def get_daily_bookings(self):
		conn = self.db_manager.get_connection()
		cursor = conn.cursor()
		sql = f"WHERE DATE(date_hired) = CURDATE();"
		cursor.execute(sql)
		rows = cursor.fetchone()
		cursor.close()
		if rows:
			bookings = []
			for row in rows:
				bookings.append(self.row_to_dict(row, cursor.description))
			return bookings
		return None


class InvoiceDAO(BaseDAO):
	def __init__(self, db_manager):
		super().__init__(db_manager, "Invoice", "invoice_id")
