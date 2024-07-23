# Project Name
Social Network

## Description
This social network application allows users to connect with each other by sending and receiving friend requests. The primary goal is to enable users to build and manage their social networks by establishing connections with other users.

## Steps to start application

1. Create a Virtual Environment

python -m venv env
source env/bin/activate 

2. Install Dependencies

pip install -r requirements.txt

## If you find any issues while intalling dependencies install manually
> pip install django djangorestframework
> pip install djangorestframework-simplejwt
> python3 -m pip install Pillow

3. Apply Migrations

python manage.py makemigrations

python manage.py migrate

4. Create a Superuser (Optional)

python manage.py createsuperuser

5. Run the Development Server

python manage.py runserver

## Open your browser and go to http://127.0.0.1:8000/ to see your Django project in action.

Since the project is added with the jinja format of html as well, user can access the api's with the UI. 

Navigate to http://127.0.0.1:8000/home/ to start accessing the application.



