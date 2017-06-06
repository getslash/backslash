.. _configuration:

Server Configuration
====================

Initial Setup
-------------

When the server first comes up, browsing to it will take you to an
initial setup screen. The screen will prompt you for the following
details:

* *Admin email/password*: This will specify the local admin account
   used to manage Backslash
* *Default Email Domain*: For users logging in with their user names,
  expecting the email domain to be automatically added upon
  authentication, you can set this optional field to be your
  organization domain.
* *Enable Google OAuth2*: Once checked, you will be able to enter the
  client ID and client secret as obtained from the Google Credentials
  console, enabling users to log in via the Google federated login
  mechanism
* *Enable LDAP*: If checked, will ask for LDAP URI and base DN,
  enabling you to log in users via your organization's LDAP service.

Optional Configuration
----------------------

Backslash uses an internal Docker volume for storing configuration
files, some of which enable specific behaviors at runtime.

In order to customize these files, you'll have to do the following on
a new instance of Backslash:

1. In the Docker compose file, change the locations referring to the
   ``conf`` volume, and set them to point at where you want to store
   the config files. For example, change ``conf:/conf`` to
   ``/my/backslash/config/files:/conf``. This needs to be done in
   several places in the configuration file
2. Start Backslash. You'll see files created in that directory,
   especially a file named ``000-private.yml``. You can now add YAML
   files to this directory, and they will be read and loaded when the
   server starts.

.. note:: The configuration directory is secret and should not be
          shared or opened for access by anyone except for
          administrators.

Create a file which will be used for your specific settings,
e.g. ``001-deployment.yml`` -- we will use this file to specify more options.

HTTPS
~~~~~

Backslash supports serving via HTTPS, in which case it prefers secure
connections over insecure ones.

To activate SSL, set the ``BACKSLASH_HOSTNAME`` environment variable
in your compose file, set ``BACKSLASH_USE_SSL`` to ``yes``, and place
your certificate and key file in your config directory, under the
names ``certificate.crt`` and ``server.key`` respectively.

Display Names
~~~~~~~~~~~~~

By default, Backslash calls test subjects "Subjects" and related
entities "Related". If you want to change these names when displayed,
you can do this via the ``display_names`` config in your
``001-deployment.yml`` mentioned above::

  ...
  display_names:
    subject: microwave
    related: plate

This will make subjects be called "microwaves" in all relevant
contexts, and related entities be called "plates".

Metadata Links
~~~~~~~~~~~~~~

In some cases you may have test metadata items which are actually
links/URIs pointing at external resources. This could be Jenkins
builds, logs collected, or any other external resource related to the
test. If you want to allow quick access to those items from the test
page, you can specify it via the ``test_metadata_links`` variable::

  ...
  test_metadata_links:
     - name: Jenkins build
       key: jenkins_url
       icon: http://url/for/jenkins/icon.png

The above will add a link to the test page pointing at the Jenkins
build whenever a "jenkins_url" metadata key is found for a test
