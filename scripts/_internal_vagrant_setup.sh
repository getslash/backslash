#! /bin/bash -x

cd /vagrant/

sudo apt-get update
sudo apt-get -y install build-essential python-dev libevent-dev python-pip
sudo pip install --use-mirrors -r base_requirements.txt
sudo pip install --use-mirrors -r flask_app/pip_requirements.txt
make local_deploy
