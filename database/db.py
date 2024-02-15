import pymysql


class DatabaseManager:
    """
    A Singleton to handle connection to the database and store the
    database for DAO access. Additionally, this class will create the
    database tables if they are not yet created.
    """

    _instance = None

    # Make sure the class is a Singleton
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, host, user, password, database):
        if not hasattr(self, 'initialized'):
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.conn = None
            self.cursor = None
            self.initialized = True

    def get_connection(self):
        return self.conn

    def connect(self):
        if not self.conn:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()

    def create_tables(self):
        create_customer_table = """
        CREATE TABLE IF NOT EXISTS Customer (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            phone VARCHAR(20)
        )
        """
        create_vehicle_table = """
        CREATE TABLE IF NOT EXISTS Vehicle (
            vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(50),
            model VARCHAR(50),
            make VARCHAR(50),
            year INT,
            registration_number VARCHAR(50),
            available BOOLEAN
        )
        """
        create_booking_table = """
        CREATE TABLE IF NOT EXISTS Booking (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            vehicle_id INT,
            date_hired DATE,
            return_date DATE,
            payment_status VARCHAR(20),
            FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
            FOREIGN KEY (vehicle_id) REFERENCES Vehicle(vehicle_id)
        )
        """
        create_invoice_table = """
        CREATE TABLE IF NOT EXISTS Invoice (
            invoice_id INT AUTO_INCREMENT PRIMARY KEY,
            booking_id INT,
            total_amount FLOAT,
            payment_date DATE,
            FOREIGN KEY (booking_id) REFERENCES Booking(booking_id)
        )
        """
        self.cursor.execute(create_customer_table)
        self.cursor.execute(create_vehicle_table)
        self.cursor.execute(create_booking_table)
        self.cursor.execute(create_invoice_table)
        self.conn.commit()


    def close(self):
        if self.conn:
            self.conn.close()
