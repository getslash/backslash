Backslash
=========

![Build Status](https://secure.travis-ci.org/slash-testing/backslash.png?branch=master ) 

Backslash is a centralized service for tracking execution of automated tests.

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

Next, you will need a running instance of Postgres, with a database named *backslash*:

```
$ pg_ctl init -D /tmp/db -w
$ pg_ctl start -D /tmp/db -w
$ createdb backslash
$ python manage.py db upgrade
```

If you wish to run an out-of-the-box test server:
- install tMux (http://tmux.sourceforge.net/)
- run:
```
$ make testserver
```


If you are testing an unstable release, most chances are that you'll need the development version of `backslash-python`, the official client library for Backslash, which is available at https://github.com/vmalloc/backslash-python.

License
=======

Backslash is distributed under the BSD 3-clause license.
