==============
django-toolkit
==============

A collection of tools and helpers for use with Django.


Installation
============

You can install django-toolkit either via the Python Package Index (PyPI)
or from bitbucket.

To install using pip;

.. code-block:: bash

    pip install django-toolkit

From github;

.. code-block:: bash

    pip install git+https://github.com/alexhayes/django-toolkit.git


Usage
=====

The code is largely undocumented at this stage but should be considered stable 
for production use.

To get to a 1.0.0 release will require many more tests and documentation.


Contributing
============

You are encouraged to contribute - please fork and submit pull requests. To get
a development environment up you should be able to do the following;

.. code-block:: bash

	git clone https://github.com/alexhayes/django-toolkit.git
	cd django-toolkit
	pip instal -r requirements/default.txt
	pip instal -r requirements/test.txt
	./runtests.py

And to run the full test suite, you can then run;

.. code-block:: bash

	tox

Note tox tests for Python 2.7, 3.3, 3.4 and PyPy for Django 1.6, 1.7 and 1.8. 
You'll need to consolute the docs for installation of these Python versions
on your OS, on Ubuntu you can do the following;

.. code-block:: bash

	sudo apt-get install python-software-properties
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get update
	sudo apt-get install python2.7 python2.7-dev
	sudo apt-get install python3.3 python3.3-dev
	sudo apt-get install python2.6 python3.4-dev
	sudo apt-get install pypy pypy-dev


Authors
=======

- Alex Hayes <alex@alution.com>
