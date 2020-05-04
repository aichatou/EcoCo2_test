# EcoCo2_test
=====
poject_name = api_project
app_name = api_app
python version supported:  3.6 or greater
=====

api_app is a django application for dealing with api and panda

Quick start
-----------
1: Create a virtual env:
> pip install virtualenv
> virtualenv 'virtualenv_name'
Activate the virtualenv (go to 'virtualenv_name' folder):
> virtualenv_name/bin/activate (or virtualenv_name\Scripts\activate for Win Os)

2: Install requirements (go to manage.py folder):
> pip install -r requirements/base.txt

3: Configure database in settings file according to your local database (must be a postgresql db) and

3. Run :
> python manage.py makemigrations
> python manage.py migrate (to create the api_app models)
> python manage createsuperuser

Go to api_app/urls.py folder and uncomment the line 'path('datas/', get_data, name='get_data')'
Run  server (python manage.py runserver) and visit http://127.0.0.1:8000/api_app/datas (this process will load data in your database) 
After you see a 'Data load: Success' message, comment again the path line in url file

Visit http://127.0.0.1:8000/api_app/panda and you will see some results

6. To run test (go to manage.py folder and run):
> tox 

7. Run test with flake8
> flake8 api_app/*
 Resolve if necessary flake8 errors with autopep8 command
 