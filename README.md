Weber-Minimal
=============

![Build Status](https://secure.travis-ci.org/vmalloc/weber-minimal.png?branch=master ) 

weber-minimal is a Flask application template, intended to get you started with a Flask-powered webapp as quickly as possible. Unlike [weber-backend](https://github.com/vmalloc/weber-backend ), weber-minimal aims at a minimalistic app, with no database engine or other bells and whistles.

weber-minimal puts an emphasis on ease of deployment (with *ansible*), and not getting in your way while you focus on your actual app logic.

Getting Started
===============

1. Check out the repository
2. Go through the configuration in `flask_app/app.yml` - most configuration options there are self-explanatory, and you might be interested in tweaking them to your needs.
3. Make sure you have `virtualenv` installed
4. Run the test server to experiment:
```
$ python manage.py testserver
```

Installation/Deployment
=======================

See `INSTALLING.md`

Development
===========

To start developing and testing, bootstrap the development environment with:

```
$ python manage.py bootstrap --develop
```

License
=======

Weber is distributed under the BSD 3-clause license.
