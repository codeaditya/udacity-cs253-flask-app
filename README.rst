========================
Udacity CS 253 Flask App
========================

This is a Flask_ App based on `Udacity's CS253 Course on Web Development`__,
taught by Steve Huffman with Sean Bennett as the developer of this course. I
have used Flask to build the app, although the course is actually taught using
Google App Engine.

.. _Flask: http://flask.pocoo.org/
.. __: https://www.udacity.com/course/cs253


Dependencies
------------
The app is currently written in Python 2 with Flask 0.10.1 as an external
dependency. To install all the dependencies run:

    pip install -r requirements.txt


First-run
---------
If you are executing the application for the first time, you would need to
first create the database for the application (otherwise, the apps requiring
database connection would raise an error). Follow the Configuration_ section
to first create the ``cs253/config.py`` file. Then, go to the root of the
folder and start the python shell to execute the following in it:

    >>> from cs253 import init_db
    >>> init_db()


Structure
---------
The root of the folder contains the package (folder) called ``cs253`` which
is our main application. To run the application, there is a file called
``runserver.py``. Executing the following command would start our application:

    python runserver.py

The package ``cs253`` contains the following folders:

- ``cs253/apps``: package for all the mini-apps (Blueprints) we develop during
  course
- ``cs253/lib``: package which contains the utils for cookie and password hashing
- ``cs253/schema``: Database schema definition files for sqlite3
- ``cs253/static``: All the css, fonts, javascript files go here (I am using
  Bootstrap)
- ``cs253/templates``: Templates for all our mini-apps we develop go here

And the following files:

- ``cs253/__init__.py``: This is our main file which instantiates our Flask app
  and imports all the Blueprints (mini-apps) from ``cs253/apps``
- ``cs253/cache.py``: This instantiates ``CACHE`` (``SimpleCache`` from
  Werkzeug library) which is used by Blueprints for Caching purposes
- ``cs253/config.py``: This is imported inside ``cs253/__init__.py``
- ``cs253/cs253_tests.py``: This is for unittests for our application


Configuration
-------------
We would need to create a config file at ``cs253/config.py``. The application
would import all the configuration from that file. I have got the following
config defined:

- ``DATABASE`` = ``str`` ("/path/to/sqlite3/database/file")
- ``DEBUG`` = ``bool`` (True for local, False for server)
- ``PYTHONANYWHERE`` = ``bool`` (False for local, True for server)
- ``SECRET_KEY`` = ``str`` ("random_string")
- ``IPINFODB_API_KEY1`` = ``str`` ("for getting geo co-ordinates using IP address)


Unittests
---------
Right now, the tests doesn't cover the whole of the application. Only the
following are covered:

- ``cs253/apps/birthday``
- ``cs253/apps/rot13``
- ``cs253/lib``

We can run the unittests executing the following command from the root of the
folder (``udacity-cs253-flask-app``):

    python -m unittest discover

This would discover all the unittests available and run tests through them.
All the tests are available in the ``testsuite`` package.
