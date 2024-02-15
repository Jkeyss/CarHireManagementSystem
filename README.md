**Car Hire Management System.**

**Requirements**: 
The main focus of the business is renting cars and vans, and the database is to manage the booking system.

* Vehicles are categorized into small cars (suitable for carrying up to 4 people), family cars (suitable for carrying up to 7 adults), and vans. (VEHICLE MANAGER)

* Information stored for each booking includes customer, car, date of hire and date on which the vehicle is to be returned. (BOOKING MANAGER)

* A customer cannot hire a car for longer than a week. (BOOKING MANAGER)

* If a vehicle is available, the customer's details are recorded (if not stored already) and a new booking is made. (CUSTOMER MANAGER, BOOKING MANAGER)

* Potential or existing customers can book a vehicle up to 7 days in advance depending on availability. (CUSTOMER MANAGER, VEHICLE MANAGER, BOOKING MANAGER)

* Customers must pay for the vehicle at the time of hire. (CUSTOMER MANAGER)

* On receiving an enquiry, employees are required to check availability of cars and vans. (VEHICLE MANAGER)

* An invoice is written at the time of booking for the customer. (INVOICE MANAGER)

* If the booking has been made in advance, a confirmation letter will be sent to the customer. (CUSTOMER MANAGER, BOOKING MANAGER)

* A report is printed at the start of each day showing the bookings for that particular day. (BOOKING MANAGER)  


**Deliverables**: (all deliverables should be placed on GIT (your personal Github account). and we may want to check your commits and branches.)
* An ERD diagram describes the DB design, field types, relationships, constraints, etc. ( a screenshot on your repo is fine)
* SQL which implements above ERD. (MySQL)
* A Python microservice implemented using Flask microframework that should connect to MySQL DB and have the following endpoints:
  * an endpoint to add new customer. [POST]
  * an endpoint to update customer [PUT]
  * an endpoint to delete customer [DELETE]
  * an endpoint to get customer. [GET]
  
Please don’t use ORMs and follow solid principles.