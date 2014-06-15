FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install -y python python-dev build-essential wget ca-certificates libxml2-dev libxslt1-dev python-software-properties libevent-dev git

RUN wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

RUN easy_install pip

RUN pip install virtualenv

ADD . /src

RUN cd /src && git clean -fdx && python manage.py deploy --dest docker

EXPOSE 80

CMD service redis-server start && service nginx start && supervisord -n