FROM ubuntu:16.04

env PYTHON_VERSION 3.6
env PYTHON_EXECUTABLE python$PYTHON_VERSION

env LC_ALL C.UTF-8
env LANG C.UTF-8

RUN apt-get update
RUN apt-get -y install build-essential rsync software-properties-common libpq-dev nginx curl redis-server gcc sudo libsasl2-dev libldap2-dev wget git


# nginx
RUN add-apt-repository ppa:chris-lea/nginx-devel
RUN apt-get update
RUN apt-get -y install nginx


RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get -y install nodejs

RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y $PYTHON_EXECUTABLE $PYTHON_EXECUTABLE-dev

RUN wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
RUN $PYTHON_EXECUTABLE /tmp/get-pip.py
RUN $PYTHON_EXECUTABLE -m pip install virtualenv


# dockerize
ENV DOCKERIZE_VERSION v0.3.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# build frontend
RUN npm install -g ember-cli
RUN npm install -g bower

ADD ./webapp/ /tmp/frontend/
RUN cd /tmp/frontend/ && npm install && bower install --allow-root
RUN cd /tmp/frontend/ && ember build

VOLUME /conf
VOLUME /uploads

ADD ./manage.py /src/
ADD ./etc /src/etc
ADD ./_lib /src/_lib
ADD ./deps/ /src/deps
ADD ./flask_app /src/flask_app
ADD ./migrations /src/migrations
ADD ./webapp /src/webapp

RUN cd /src && $PYTHON_EXECUTABLE manage.py bootstrap --app

RUN rsync -a --delete /tmp/frontend/ /src/webapp/

RUN rm -rf /etc/nginx/conf.d/*
RUN rm -f /etc/nginx/sites-enabled/*

EXPOSE 80 443

WORKDIR /src
