### YUF CRM (Customer Relationship Management)   
- is a web application for sale managers, directors and administrators of small-medium businesses.

### Installation:

### (Optionally)
For front-end part fully working and responsive download and unpack the following libraries in /static directory:

Library | Link
------------ | -------------
bootstrap-4.5.3 | https://getbootstrap.com/docs/4.5/getting-started/download/
fontawesome 4.0 | https://fontawesome.com/v4.7.0/get-started/

To avoid problems with paths the /static directory will look like:
/static/bootstrap-4.5.3
/static/fontawesome

... or connect them through CDN or other source of your choice

### Make venv either in your IDE or by executing command:
python3 -m venv /path/to/new/virtual/environment

### Then install requirements:
pip install -r requirements.txt

### Then create DB and apply migrations:
python manage.py makemigrations
python manage.py migrate

### (Optionally)
python manage.py createsuperuser

### Then runserver:
python manage.py runserver

### All done!
The application homepage is located at http://127.0.0.1/client  
(Optionally)  
You can use pure Django's backend at http://127.0.0.1/admin

The application "client" is made for customer records tracking and marketing strategy tracking (client origin, type).  
It will be further extended by Order, Product, Cart and other applications. 


### Requirements:

asgiref==3.3.1  
Django==2.2.15  
Pillow==8.0.1  
pytz==2020.4  
sqlparse==0.4.1

### To Do:

- Login on the first page (Google OAuth)
- Registration via Gmail
- Profile, roles and groups for User
- Landing page with main activity routes (app home)
- Cart
- Order
- Product

