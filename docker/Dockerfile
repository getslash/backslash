FROM python:3.6

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN pip install virtualenv

# nginx
ENV NGINX_VERSION 1.11.10-1~jessie
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
        && echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
        && apt-get update \
        && apt-get install --no-install-recommends --no-install-suggests -y \
                                                ca-certificates \
                                                nginx=${NGINX_VERSION} \
                                                nginx-module-xslt \
                                                nginx-module-geoip \
                                                nginx-module-image-filter \
                                                nginx-module-perl \
                                                nginx-module-njs \
                                                gettext-base \
        && rm -rf /var/lib/apt/lists/*
RUN apt-get update

RUN apt-get -y install build-essential rsync python3 python3-pip python3-dev software-properties-common libpq-dev nginx curl redis-server gcc sudo libsasl2-dev libldap2-dev wget
RUN apt-get -y install nodejs

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

RUN cd /src && python manage.py bootstrap --app

RUN rsync -a --delete /tmp/frontend/ /src/webapp/

RUN rm -rf /etc/nginx/conf.d/*
RUN rm -f /etc/nginx/sites-enabled/*

EXPOSE 80 443

WORKDIR /src
