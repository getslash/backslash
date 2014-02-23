Weber-Backend
=============

![Build Status](https://secure.travis-ci.org/vmalloc/weber-backend.png?branch=master ) 

weber-backend is a Flask application template, intended to get you started with a Flask-powered webapp as quickly as possible. weber-backend includes a database layer through Flask-SQLAlchemy, migrations through Alembic, asynchronous tasks via RQ and Redis, and more.

weber-backend puts an emphasis on ease of deployment (with *ansible*), and not getting in your way while you focus on your actual app logic.

Getting Started
===============

1. Check out the repository
2. Go through the configuration in `src/app.yml` - most configuration options there are self-explanatory, and you might be interested in tweaking them to your needs.
3. Make sure you have `virtualenv` installed
4. Run the test server to experiment

	$ make testserver

Database Migrations
===================

Create a new revision automatically with:

	$ make db_revision

And migrate with

	$ make db_migrate

Migration is done automatically on deployment

Deployment
==========

Weber provides several deployment options:

1. Deployment to production/staging:

		$ make deploy

  or

		$ make deploy_staging

  **Note**: for production/staging deploy you must edit the relevant inventory file at ``ansible/inventories/`` (See [Ansible's documentation](http://www.ansibleworks.com/docs/intro_inventory.html ) for more details)

2. Deployment to vagrant:

		$ make deploy_vagrant

3. Deployment to local host:

		$ make deploy_localhost

License
=======

Weber is distributed under the BSD 3-clause license.
