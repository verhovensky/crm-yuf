### YUF CRM (Customer Relationship Management)   
YUF (Your Ultimate Friend) - is a responsive web application (operational CRM) for managing all your company's relationships and interactions with customers and potential customers.
Suitable for sale managers, directors and administrators of small-medium businesses.

# Installation

python3 -m venv /path/to/venv 

source /path/to/venv/bin/activate

pip install -r requirements.txt

#### Create & connect db backend

python manage.py makemigrations client order account product

python manage.py migrate

#### Then runserver
python manage.py runserver

### To Do:

- Home app (main page)
- UserProfile statistics
- Dockerize

### Improvements
- Google OAuth Login and registration



