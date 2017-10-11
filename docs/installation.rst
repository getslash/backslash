.. _installation:

Installation
===============

There are several ways to get Backslash up and running, but the simplest way is probably using *Docker* and *docker-compose*.

Step 1: Install Prerequisites
-----------------------------

To run Backslash as a Docker container you'll need to have Docker
installed. This is well covered in the `Docker installation guide
<https://docs.docker.com/engine/installation/>`_. You will also need
to install *docker-compose*, which is covered `here
<https://docs.docker.com/compose/install/>`_.

Step 2: Obtain the Compose File
-------------------------------

In order for Backslash to run, it needs its various supporting
services to run in adjacent containers. *docker-compose* takes care of
this by starting the various services in their respective containers
and linking the various pieces together, but in order to do so it
needs the configuration file that specifies the deployment.

You can download the reference docker-compose file from the
`Backslash repository
<https://github.com/getslash/backslash/blob/master/docker/docker-compose.yml>`_::

  $ mkdir /opt/backslash
  $ mkdir /opt/backslash/docker
  $ curl https://raw.githubusercontent.com/getslash/backslash/master/docker/docker-compose.yml > /opt/backslash/docker/docker-compose.yml

.. note:: The docker-compose reference file might change as versions
          progress and more services are needed or modifications to
          existing services are needed. You will need to keep track of
          this file before upgrading.

Step 3: Configure Backslash to Run as a Service
-----------------------------------------------

Once you have the compose file in place, you can configure your
service to run on your host server. We recommend using *systemd* to
achieve this (which is shown here), but you can use other mechanisms
or approaches as you see fit.

Create a unit description file -- we'll call it here
``backslash-docker`` -- and place it in systemd's configuration
directory as ``/etc/systemd/system/backslash-docker.service``::

  # /etc/systemd/system/backslash-docker.service
  [Unit]
  Description=Backslash test reporting service
  Requires=docker.service
  After=docker.service

  [Service]
  Type=oneshot
  RemainAfterExit=yes
  WorkingDirectory=/opt/backslash/docker
  ExecStartPre=-/usr/local/bin/docker-compose -f docker-compose.yml -p backslash down
  ExecStart=/usr/local/bin/docker-compose  -f docker-compose.yml -p backslash up -d
  ExecStop=/usr/local/bin/docker-compose -f docker-compose.yml -p backslash down

  [Install]
  WantedBy=multi-user.target

Once you have created the unit file you can enable it to start on
boot::

  $ systemctl daemon-reload
  $ systemctl enable backslash-docker


Step 4: Start Backslash
-----------------------

You can start Backslash by running::

  $ systemctl start backslash-docker

.. note:: The initial execution will take longer than usual because
          the supporting images have to be fetched from the
          Internet. If you want to see the progress yourself, you can
          consider running docker-compose manually on the first run


Now that the server is up and running, it's time to configure your
server. You can read about it in the :ref:`configuration` section.



Upgrade 
-------

The way to upgrade an existing deployment to the latest version is:
1. update the docker image:
  $ docker pull getslash/backslash
2. restart the daemon:
  $ sudo systemctl restart backslash-docker
