from ubuntu:precise

RUN apt-get update

RUN apt-get install -y python python-dev build-essential wget ca-certificates libxml2-dev libxslt1-dev python-software-properties libevent-dev

RUN wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python

RUN easy_install pip

RUN pip install virtualenv

ADD . /src

RUN cd src && make env

WORKDIR /src

EXPOSE 8000

CMD .env/bin/uwsgi --http 0.0.0.0:8000 -b 16384 --home .env --module flask_app.app --callable app -p 10

