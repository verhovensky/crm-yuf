## YUF CRM   
YUF CRM - is a responsive web application (operational CRM) for managing company's relationships and interactions with customers, products and orders.

### Features

* Custom user profile statistics (closed sales, total sales amount)
* Three basic Groups Admins, Sellers, Managers
* User login, registration, password restoration
* Groups and permission automatic creation by management command
* Automatic expiration of Order by time
* Order status partially change depending on user group
* Responsive frontend design
* Email password restore
* Product quantity and price calculation in decimal
* Product quantity check before order creation
* Custom slugs for product

### Installation

Create .env file from template, fill all necessary variables<br>

docker-compose build<br> 

docker-compose up<br> 

Application available at 127.0.0.1:800<br>

BaseAdmin (administrator user) will be created automatically, credentials will be displayed in console.<br>

Use<br>
docker-compose stop && docker-compose down<br>
to stop and remove application and its services <br>

### To Do:

- CRUD Category, nested Categories
- Category CRUD on frontend
- Remove Celery (make use of DurationField and model methods for Order status updates) 
- Display/hide action buttons depending on Group
- Correct permission denied pages
- Forms, buttons etc. fixes
- Home app (main page)
- Update Django version and deps
- Tests & demo data