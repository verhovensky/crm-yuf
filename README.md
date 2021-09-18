### YUF CRM (Customer Relationship Management)   
YUF (Your Ultimate Friend) - is a responsive web application (operational CRM) for managing all your company's relationships and interactions with customers and potential customers.
Suitable for sale managers, directors and administrators of small-medium businesses.

# Installation

python3 -m venv /path/to/venv 

source /path/to/venv/bin/activate

pip install -r requirements.txt

#### Create & connect db backend

python manage.py makemigrations

python manage.py migrate

#### Then runserver
python manage.py runserver


# Requirements:

beautifulsoup4==4.9.3 <br>
Django==2.2.15 <br>
django-bootstrap-datepicker-plus==3.0.5 <br>
django-bootstrap4==3.0.1 <br>
Pillow==8.0.1 <br>
pytz==2021.1 <br>
soupsieve==2.2.1 <br>
sqlparse==0.4.1 <br>

### To Do:

- Dockerize
- User groups and permissions
- Landing page with main activity routes (app home)

### Improvements
- Google OAuth Login and registration
- Django REST API
- IP based calls app based on Asterisk



