# django-filehosting
Simple filehosting (filesharing) application developed with Django and Celery


## About
The user can upload the file and specify the time in minutes until expiration. 
After the uploading, the user is redirected to the info page about the uploaded file.
The filename, file size, time to expiration, and link for file downloading are 
displayed on the info page. Using the link for downloading, anyone can download the file.
After the specified time elapsed, the file should be removed from the storage and 
the info page and the download link are now not accessible (returns 404 Not found).


## Technology stack
The following major technologies were used:
* Django 3.0.8
* Celery 4.4.6

For Celery, you can use either Redis or RabbitMQ backend (should be installed and
properly configured).

The current implementation uses SQLite database for simplicity.


## How to run
1. Clone the repo: `git clone https://github.com/dfesenko/django-filehosting.git`. 
Go inside the `django-filehosting` folder: `cd django-filehosting`.
2. Create a virtual environment: `python -m venv venv`.
3. Activate virtual environment: `source venv/bin/activate`.
4. Install dependencies into the virtual environment: `pip install -r requirements.txt`.
5. Install Redis:  `sudo apt update`, `sudo apt install redis-server`. Alternatively, you 
can install RabbitMQ.
6. Run Redis  (in a separate Terminal window): `redis-server`. Or run RabbitMQ server.
7. You can change the settings in the `filehosting/settings.py` file. For example, the maximum 
file size or the directory for files storing can be set there. Please be aware, that the 
current settings are for development purposes, and when deploying, several changes must be made.
8. Perform migrations: `python manage.py makemigrations`, `python manage.py migrate`. This should
create the file that represent the SQLite db (if you use this database backend).
9. Run Celery workers (in a separate Terminal window, but with activated virtual 
environment and from the `django-filehosting` directory): 
`celery worker -A filehosting --loglevel=debug --concurrency=4`.
10. Run Celery beat to be able to execute regular periodic task: `celery -A filehosting beat`. This
is needed to remove expired files once in 30 minutes. 
10. Run Django server: `python manage.py runserver`.
11. The application should be available in the browser: `localhost:8000`.


## Important notes about app's workflow
There is the FileObject model that has 3 fields - file, uploaded_at, and expired_at. The uploaded_at 
field is filled automatically when the new model object is created (the user uploads the file).
The expired_at field is computed using the uploaded_at field and the time in minutes specified by the user
(expiration time). When the user tries to access the file (for download or for viewing the info page),
the view checks whether the "now" time is less than the expired_at time. If not, the 404 page is returned.
But the file is still in the database. It is removed only after running the periodic Celery job, which 
is triggered once per 30 minutes (this can be changed in the `filehosting/celery.py` file) 
and deletes all expired file objects from the database and files from the server in a bulk mode.
