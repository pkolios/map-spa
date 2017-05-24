Map Single Page App
===================

Map Single Page App (map-spa in short) allows you to click on map and store
the address of the point you clicked on, as long as it is a real address.

This is a single page application that consists of a full viewport map and a
list of the selected addresses.

Installation
------------
For docker setup you can get the development environment up and running with
the following commands:

1. Build the docker image with:

::

    docker build -t map-spa .

2. Run a shell inside the image with:

::

    docker run -v $(pwd):/usr/src/app -p 8000:8000 -it --rm --name map-spa map-spa /bin/bash

3. Prepare the database:

::

    cd mapsite/
    python manage.py migrate

4. Run the development server:

::

    python manage.py runserver 0.0.0.0:8000


If you prefer to setup the app without docker you can do the following:

1. Prepare the virtual environment

::

    virtualenv env && source env/bin/activate && pip install -r requirements.txt

3. Prepare the database:

::

    cd mapsite/
    python manage.py migrate

4. Run the development server:

::

    python manage.py runserver 0.0.0.0:8000


Configuration
-------------

The configuration of this app is located in the standard ``django.settings``
module as well as in the ``mapsite/client_secrets.json`` file for fusion tables.
Please make sure you update both files with your own settings before using the
app.

To use the google maps API you must create and enable an api key as specified
in the documentation https://developers.google.com/maps/documentation/javascript/get-api-key

To use the google fusion tables you first set them up as specified in the
documentation https://developers.google.com/fusiontables/

*WARNING* This app is not ready for production!


Testing
-------

This app has some basic test coverage. You can run the tests with the following
command:

::

    python manage.py test


Documentation
-------------

The code in this application is quite minimal, given the short time that was
available for implementation. I tried to keep the use of external modules to
a minimum (few python packages, pure javascript code, almost no styling).
It has only been tested on Chrome.

Some things for furterh consideration:

- Clean up configuration and remove sensitive data
- Use async workers for updating Google Fusion Tables (celery)
- Paginate the results to achieve better scaling
- Add static file minifiers / uglyfiers

License
-------
MIT licensed. See the `LICENSE <https://github.com/pkolios/map-spa/blob/master/LICENSE>`_ file for more details.
