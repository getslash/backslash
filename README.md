Weber
=====

![Build Status](https://secure.travis-ci.org/vmalloc/weber.png?branch=master,dev ) 

Weber is a ready-to-deploy skeleton for building in-house web-based apps. Its goal is to provide a "batteries included" approach for rapid webapp development for small/medium scale apps.


Getting Started
===============

1. Check out the repository
2. Go through the configuration in `src/app.yml` - most configuration options there are self-explanatory, and you might be interested in tweaking them to your needs.
3. Install base requirements:

	$ pip -r base_requirements.txt

3. If needed, create a user:

	$ python manage.py create_user -e user@somedomain.com -p PASSWORD

4. Run the test server to experiment:

	$ python manage.py testserver

5. When you're ready to deploy, run the following:

	$ python scripts/deploy some.host.address


License
=======

Weber is distributed under the BSD 3-clause license.
