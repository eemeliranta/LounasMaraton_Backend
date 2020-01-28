# Lounas Maraton Application API

A Django backend to be used with Lounas Maraton mobile applicaiton

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* [Python 3](https://www.python.org/) - 3.x

### Installing

* Install the Python, navigate to your the project directory and create a virtual enviroment with:
```
python -m venv venv
```

* Enter the virtual enviroment with by opening the activate file in your command line: 
```
\LounasMaraton\venv\Scripts\activate
```

* Install the prerequisite packages with 
```
pip install -r requirements.txt
```

* Run database migrations 
```
python manage.py makemigrations backend
python manage.py migrate
```

* Create a superuser 
```
python manage.py createsuperuser --username admin
```

* Load some seed data 
```
python manage.py loaddata seed.json
```

* Start the server at localhost:8000
```
python manage.py runserver
```
