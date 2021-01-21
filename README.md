### YUF CRM (Customer Relationship Management)   
YUF (Your Ultimate Friend) - is a responsive web application (operational CRM) for managing all your company's relationships and interactions with customers and potential customers.
Suitable for sale managers, directors and administrators of small-medium businesses.

### Installation

### Make venv either in your IDE or by executing command:
python3 -m venv /path/to/new/virtual/environment

### Then install requirements
pip install -r requirements.txt

### Then create DB and apply migrations

### Then runserver
python manage.py runserver

### All done!
The application homepage is located at http://127.0.0.1/client  
(Optionally)  
You can use pure Django's backend at http://127.0.0.1/admin

The Client app is made for customer analytics and tracking.
The Product app is made for stock arrival and sales calculation.

### Requirements:

asgiref==3.3.1  
Django==2.2.15  
Pillow==8.0.1  
pytz==2020.4  
sqlparse==0.4.1

### To Do:

- Order model
- User groups and permissions
- Landing page with main activity routes (app home)
- Google OAuth Login and registration
- Django REST API
- IP based calls app based on Asterisk



