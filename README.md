# EcoCo2_test
=====<br />
poject_name = api_project<br />
app_name = api_app<br />
python version supported:  3.6 or greater<br />
=====<br />

api_app is a django application for dealing with api and panda<br />

Quick start
-----------
1: Create a virtual env:<br />
> pip install virtualenv<br />
> virtualenv 'virtualenv_name'<br />
Activate the virtualenv (go to 'virtualenv_name' folder):<br />
> virtualenv_name/bin/activate (or virtualenv_name\Scripts\activate for Win Os)<br />

2: Install requirements (go to manage.py folder):<br />
> pip install -r requirements/base.txt<br />

3: Configure database in settings file according to your local database (must be a postgresql db) and run :<br />
> python manage.py makemigrations<br />
> python manage.py migrate (to create the api_app models)<br />
> python manage createsuperuser<br />

4.Go to api_app/urls.py folder and uncomment the line 'path('datas/', get_data, name='get_data')'<br />

5.Run  server (python manage.py runserver) and visit http://127.0.0.1:8000/api_app/datas (this process will load data in your database) <br />
After you see a 'Data load: Success' message, comment again the path line in url file<br />

Visit http://127.0.0.1:8000/api_app/panda and you will see some results<br />

6. To run test (go to manage.py folder and run):<br />
> tox <br />

7. Run test with flake8<br />
> flake8 api_app/views.py (for example)<br />
 Resolve if necessary flake8 errors with autopep8 command<br />
 