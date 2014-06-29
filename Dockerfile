FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install -y software-properties-common python-software-properties

RUN apt-add-repository ppa:nginx/stable

RUN apt-add-repository ppa:chris-lea/node.js

RUN apt-get update

RUN apt-get install -y python python-dev build-essential wget ca-certificates libxml2-dev libxslt1-dev python-software-properties libevent-dev git nginx redis-server

RUN sudo apt-get -y install libpq-dev

RUN apt-get -y install nodejs

RUN wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

RUN easy_install pip

RUN pip install virtualenv

ADD ./src_pkg.tar /tmp/

RUN mkdir /src /persistent /persistent/config

ENV CONFIG_DIRECTORY /persistent/config

RUN cd /src && tar xvf /tmp/src_pkg.tar

RUN cd /src && rm -rf .env && find . -name "*.pyc" -delete

RUN cd /src && python manage.py bootstrap --app

RUN rm -rf /etc/nginx/sites-enabled/*

RUN cd /src && python manage.py generate_nginx_config /etc/nginx/sites-enabled/webapp

RUN cd /src && python manage.py frontend build

EXPOSE 80

ENV SQLALCHEMY_DATABASE_URI postgresql+psycopg2://postgres@$DB_PORT_5432_TCP_ADDR:$DB_PORT_5432_TCP_PORT/db

CMD service redis-server start && service nginx start && cd /src && python manage.py ensure-secret /persistent/config/000-secret.yml && python manage.py db ensure && python manage.py db upgrade && python manage.py run_uwsgi
