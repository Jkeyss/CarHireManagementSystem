-- Create Database
CREATE DATABASE car_hire_management_system_db CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci';

-- Create User
CREATE USER 'car_management_admin'@'localhost' IDENTIFIED BY 'DevDB';

-- Grant Privileges
GRANT ALL PRIVILEGES ON car_hire_management_system_db.* TO 'car_management_admin'@'localhost';

-- Flush Privileges
FLUSH PRIVILEGES;