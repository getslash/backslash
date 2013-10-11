Weber
=====

![Build Status](https://secure.travis-ci.org/vmalloc/weber.png?branch=master,dev ) 

Weber is a Flask application template, intended to get you started with a Flask-powered webapp as quickly as possible.

Weber puts an emphasis on ease of deployment (with *ansible*), and not getting in your way while you focus on your actual app logic.

Getting Started
===============

1. Check out the repository
2. Go through the configuration in `src/app.yml` - most configuration options there are self-explanatory, and you might be interested in tweaking them to your needs.
3. Make sure you have `virtualenv` installed
4. Run the test server to experiment

	$ make testserver

5. When you're ready to deploy, run the following (you'll need ansible installed on your machine):

	$ make deploy target=myhost.mydomain.com

License
=======

Weber is distributed under the BSD 3-clause license.
