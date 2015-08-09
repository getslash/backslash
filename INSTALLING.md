# Installation and Deployment

## Regular Installation using Ansible

Edit the file `ansible/inventories/production`, and fill in the name of your destination server. Here is an example of such a file:

```
[webapp]
my.server.com ansible_ssh_user=root
```

Then run:

```
python manage.py deploy --dest production
```

## Other Destinations

In addition to a destination server, you can also deploy to *staging*, or a beta server to test your deployment before hitting production.

`manage.py deploy --dest` also understand the *vagrant* argument, causing installation on a vagrant instance, and *localhost* meaning deploying on the local machine.
