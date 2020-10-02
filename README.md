# Backslash

|                       |                                                                                    |
|-----------------------|------------------------------------------------------------------------------------|
| Build Status          | ![Build Status](https://secure.travis-ci.org/getslash/backslash.png?branch=master) |
| Supported Versions    | ![Supported Versions](https://img.shields.io/badge/python-3.6-green.svg)    |

Backslash is a centralized service for tracking execution of automated tests.

* [Official website](https://getslash.github.io/backslash)
* [Documentation](https://backslash.readthedocs.io/en/latest/)
* [Python client](https://github.com/getslash/backslash-python)

## Development

### Initial Setup and Prerequisites

Make sure you install all requirements (including development dependencies) through `pipenv`:

``` shell
$ pipenv install -d
```

Additionally, you will need:

* Postgres (>=9.5) running locally
* Redis running locally

You will need a running database called `backslash` locally. Make sure you have Postgres running, and then run:

``` shell
createdb backslash
```

Then run DB migrations:

``` shell
pipenv run manage db upgrade
```

### Running Tests

``` shell
$ make test
```

# License
Backslash is distributed under the BSD 3-clause license.
