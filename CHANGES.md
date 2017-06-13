# Changelog

## Version 2.8.0

* Initial support for parallel runs
* Add option to configure auxiliary services for supporting custom APIs
* Added documentation for installation, deployment and configuration (See https://backslash.readthedocs.org)

## Version 2.7.0

* You can now search for sessions by contained test name via the `test = my_test_name` search clause
* You can now jump to the "last" page in the session tests view
* Added monitoring compatible with Prometheus (both natively via `/metrics` and the postgres exporter on port 9187)
* Tracebacks and errors are significantly improved, and now support collapsing of `self` attributes, copying the full exception to the clipboard and more
* Backslash now supports a newer way of uploading tracebacks via streaming uploads, improving performance on large tracebacks
* You can now search for sessions by status
* Deployment moved to Docker, ditched Ansible

## Version 2.6.3

* Many small UI/UX fixes and tweaks

## Version 2.6.0

* Support test parameters display for parameetrized tests
* Session information sidebar in session view is now collapsible, giving more room to examine tracebacks or exceptions
* Backslash now properly handles interrupted tests and sessions
* Add ability to search by product version
* Add option to control the landing page (all sessions/my sessions)
* Add session breakdown info to left information bar
* Add option to quickly expand side information bars for sessions
* Backslash now documents test indices
* J/K in test view jumps to next/previous test
* Comments can now be edited and deleted
* Comments now support markdown syntax for formatting

## Version 2.5.0

* Proxy users can now run sessions for emails that do not exist yet. This will create stub user records to be populated later
* Added session search
* Misc. performance improvements

## Version 2.4.0

* Support session labels, added through API

## Version 2.3.3

* Times are humanized by default again (accidental regression)

## Version 2.3.2

* Minor bug fixes

## Version 2.3.1

* Minor bug fixes

## Version 2.3.0

* Added basic support for searching tests and sessions using a query syntax
* Session view now displays durations
* Sessions and tests now have a preview of the latest comment made on them, when you hover over them. You can also hit `c` to toggle showing the latest comment on all items in view
* Many bugs fixed
  * Status display for tests inside abandoned sessions

## Version 2.2.0

* Major overhaul of UI
   * Session and test details are now nested views
   * Clearer flow between session, session errors/warnings, single tests and test errors/warnings
   * Simpler browsing of error details
   * Clearer indication of test/session statuses via status icons
* Many bugfixes and small improvements


## Version 2.1.0

* Added LDAP support
* Added initial setup wizard
* Added support for test parametrization info
* Added quick-jump to go to test subjects, users or test/session ids
* Added a user preferences mechanism for controlling various options, starting with the time format display
* Many bugfixes and small improvements

## Version 2.0.0

* First official release
