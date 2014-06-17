FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install -y software-properties-common python-software-properties

RUN apt-add-repository ppa:nginx/stable

RUN apt-get update

RUN apt-get install -y python python-dev build-essential wget ca-certificates libxml2-dev libxslt1-dev python-software-properties libevent-dev git nginx redis-server

RUN wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

RUN easy_install pip

RUN pip install virtualenv

ADD . /src

RUN cd /src && rm -rf .env && find . -name "*.pyc" -delete

RUN cd /src && python manage.py bootstrap --app

RUN rm -rf /etc/nginx/sites-enabled/*

RUN cd /src && python manage.py generate_nginx_config /etc/nginx/sites-enabled/webapp

EXPOSE 80

CMD service redis-server start && service nginx start && cd /src && python manage.py run_uwsgi
