# Reddit RDBMS

This is an application written for Project 1.3 for **S4111 - Introduction to Databases** at [Columbia University](http://www.columbia.edu/) in the [Computer Science Department](http://www.cs.columbia.edu/).

The web application front-end is written in Python using the following modules below and relies on a database backend running PostgreSQL 9.3.

- [sqlalchemy](http://www.sqlalchemy.org/)
- [Flask](http://flask.pocoo.org/)

The theme is based off of [Bootstrap CSS](http://getbootstrap.com/). Table formatting and in-result contextual searching is done via [DataTables for jQuery](https://datatables.net/).

It can be accessed [here](http://s4111.cu.moffitt.de).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

The application was built on Azure using Ubuntu 14.04.3.

Additional packages needed:
```
sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 python-virtualenv python-dev
sudo pip install flask psycopg2 sqlalchemy click
```

### Installing

Extract the "webserver" directory to a location on the webserver and configure the "server.py" settings to match your requirements.

```
DATABASEURI = "postgresql://<userID>:<userPassword>@w4111vm.eastus.cloudapp.azure.com/w4111"
```

Launch the application

```
sudo python webserver/server.py
```

The application should now be available on http://<serverIP>:8111

## Authors

* **Marshall Van Loon** - [mhv2109@columbia.edu](mailto:mhv2109@columbia.edu)
* **Zachary Moffitt** - [znm2104@columbia.edu](mailto:znm2104@columbia.edu)


## Acknowledgments & Notes

* Written in a few days under Summer Session time constraints. The code should be cleaned up (time permitting) and comments updated.
