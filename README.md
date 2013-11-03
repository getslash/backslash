Weber
=====

![Build Status](https://secure.travis-ci.org/vmalloc/weber-minimal.png?branch=master ) 

Weber is a Flask application template, intended to get you started with a Flask-powered webapp as quickly as possible.

Weber puts an emphasis on ease of deployment (with *ansible*), and not getting in your way while you focus on your actual app logic.

Variants
========

* *weber-minimal* - includes deployment infrastructure and basic flask skeleton only. Useful for very small, headless, web services or very tiny apps
* *weber-backend* - includes database installation (Postgres by default) and Flask-SQLAlchemy, along with db migrations.

Getting Started
===============

1. Check out the repository
2. Go through the configuration in `src/app.yml` - most configuration options there are self-explanatory, and you might be interested in tweaking them to your needs.
3. Make sure you have `virtualenv` installed
4. Run the test server to experiment

	$ make testserver


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
