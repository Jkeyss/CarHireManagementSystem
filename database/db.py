import pymysql
from decouple import Config, RepositoryEnv


class DatabaseManager:
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
            CustomerID INT AUTO_INCREMENT PRIMARY KEY,
            FirstName VARCHAR(50),
            LastName VARCHAR(50),
            Email VARCHAR(100),
            Phone VARCHAR(20)
        )
        """
        create_vehicle_table = """
        CREATE TABLE IF NOT EXISTS Vehicle (
            VehicleID INT AUTO_INCREMENT PRIMARY KEY,
            Type VARCHAR(50),
            Model VARCHAR(50),
            Make VARCHAR(50),
            Year INT,
            RegistrationNumber VARCHAR(50),
            Available BOOLEAN
        )
        """
        create_booking_table = """
        CREATE TABLE IF NOT EXISTS Booking (
            BookingID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT,
            VehicleID INT,
            DateHired DATE,
            ReturnDate DATE,
            PaymentStatus VARCHAR(20),
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
            FOREIGN KEY (VehicleID) REFERENCES Vehicle(VehicleID)
        )
        """
        create_invoice_table = """
        CREATE TABLE IF NOT EXISTS Invoice (
            InvoiceID INT AUTO_INCREMENT PRIMARY KEY,
            BookingID INT,
            TotalAmount FLOAT,
            PaymentDate DATE,
            FOREIGN KEY (BookingID) REFERENCES Booking(BookingID)
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


if __name__ == "__main__":
    DOTENV_FILE = '../envs.env'
    config = Config(RepositoryEnv(DOTENV_FILE))

    mysql_config = {
        'host': config('DB_HOST'),
        'user': config('DB_USER'),
        'password':  config('DB_PASSWORD'),
        'database': config('DB_DATABASE')
    }

    db_manager = DatabaseManager(**mysql_config)
    db_manager.connect()
    db_manager.create_tables()
    db_manager.close()