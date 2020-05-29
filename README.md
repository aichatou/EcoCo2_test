# EcoCo2_test
=====<br />
poject_name = api_project<br />
app_name = api_app<br />
python version supported:  3.6 or greater<br />
=====<br />

api_app is a django application for dealing with api and panda<br />

Quick start
-----------
1: Go to EcoCo2_test-master folder and create a new virtual env:<br />
> pip install virtualenv (if necessary)<br />
> virtualenv 'virtualenv_name'<br />
Activate the virtualenv (go to 'virtualenv_name' folder):<br />
> virtualenv_name/bin/activate (or virtualenv_name\Scripts\activate for Win Os)<br />

2: Install requirements (be sure you are in manage.py folder):<br />
> pip install -r requirements/base.txt (if some errors, try to install package one by one with 'pip install package_name' command)<br />

3: Create a superuser for managing data in django admin interface <br/>
> python manage createsuperuser<br />

4: Run  server:
> python manage.py runserver (if some errors, try 'python manage.py check' command for more details) <br />

5: Visit http://127.0.0.1:8000/api_app/panda (some results will be displayed) <br />
(List of datas are displayed on  http://127.0.0.1:8000/api_app/co2List/  and data can be managed on  http://127.0.0.1:8000/admin) <br />

6: To run test (go to manage.py folder and run):<br />
> tox <br />

7.Run flake8 test (optional) <br />
> flake8 api_app/views.py (for example)<br />
Resolve if necessary flake8 errors with autopep8 --in-place command<br />

 