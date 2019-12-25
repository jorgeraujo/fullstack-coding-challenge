# Unbabel Full Stack Challenge

Project for the unbabel full stack position challenge

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

It's a good idea to create an virtual environment for the project.

```
python3 -m venv env
```

### Installing

This will get all of the dependencies for the flask app to run.

```
pip install -r requirements.txt
```

for the app to run it need a database, using psql or some postgres app like postgres.app create a database, for this case we are going to create a database called unbabel.

```
=# create database unbabel ;
```
The app pickes the database from a environment variable called `DATABASE_URL`, in case you are running the database locally and if it's called unbabel the db address to export should be:
```
export DATABASE_URL=postgresql://localhost:5432/unbabel
```
In order to create the tables based on the models of the app im using flask, so to run the table generation run :
```
flask db init
flask db migrate
flask db upgrade
```
The `config.py` file has some more configurations that need to be set for the app to run:
```
TRANSLATION_CALLBACK = 'address_for_the_unbabel_translation_callback'
UNBABEL_API_KEY = 'some_api_key'
UNBABEL_API_USERNAME = 'some_api_username'
```
When running the app locally the callback should exposed to the internet, to do this you can use some tool like [ngrok](https://ngrok.com/) to hande this.

To finally run the app:
```
export FLASK_APP=main.py
flask run
```

## Running the tests

To run the backend tests:
```
python -m pytest -vv
```

To run the frontend tests:
```
cd fullstack-coding-challenge/tests
npm install
npm test
```

### Stack Used

For the backend I just used Flask, Postgres and SQLAlchemy. For the frontend for the sake of simplicity I just used vanilla JS and bootstrap instead of a bulkier framework like React or Angular because the frontend looked simple enough for that.

In order to get the server to communicate with the client when the translation was done I used sockets, so the user doesn't have to reload the page to check the new translations.