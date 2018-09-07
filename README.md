# FASTFOODFAST-API
![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/davishooly/FASTFOODFAST-API.svg?branch=develop)](https://travis-ci.org/davishooly/FASTFOODFAST-API)
[![Coverage Status](https://coveralls.io/repos/github/davishooly/FASTFOODFAST-API/badge.svg?branch=develop)](https://coveralls.io/github/davishooly/FASTFOODFAST-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/a236552c6eda78af4c69/maintainability)](https://codeclimate.com/github/davishooly/FASTFOODFAST-API/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9808cd8c1dfd4695a43de932c7af6e45)](https://www.codacy.com/app/davishooly/FASTFOODFAST-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=davishooly/FASTFOODFAST-API&amp;utm_campaign=Badge_Grade)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


# Fast Food Fast

Fast food fast is a food delivery application.

## How it Works

- An admin creates food items
- A normal user creates an account and can login
- A logged in user can view available food items created by the admin
- A user chooses on a food item and makes an order
- An Admin can accept or reject the order request from a user
- A user gets notified on his/her order status
- Accepted orders are delivered

## Prerequisite

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Virtua Environment](https://virtualenv.pypa.io/en/stable/installation/)

# Installation and Setup

Clone the repository below

```
git clone https://github.com/davishooly/FASTFOODFAST-API.git
```

### Create and activate a virtual environment

    virtualenv env --python=python3.6

    source env/bin/activate

### Install required Dependencies

    pip install -r requirements.txt

## Running the application

```bash
$ export FLASK_APP = run.py

$ export MODE = development

$ flask run
```

## Endpoints Available

| Method | Endpoint                        | Description                           |
| ------ | ------------------------------- | ------------------------------------- |
| POST   | /api/v1/auth/signup             | sign up a user                        |
| POST   | /api/v1/auth/login              | login a user                          |
| POST   | /api/v1/fooditems               | post a fooditem                       |
| GET    | /api/v1/fooditems               | get all available fooditems           |
| POST   | /api/v1/fooditems/<{id}>/orders | post an order on a specific food item |
| GET    | /api/v1/fooditems/orders        | get the all food orders               |
| PUT    | /api/v1/fooditems/orders/<{id}> | update on the status of an order      |
| GET    | /api/v1/fooditems/orders/<{id}> | get a specific food order             |
| DELETE | /api/v1/fooditems/<{id}>        | delete a specific order               |
| DELETE | /api/v1/fooditems/orders/<{id}> | delete a specific food order          |

### Testing

    nosetests

    - Testing with coverage

    nosetests --with-coverage --cover-package=app

### Author

Kimame Davis