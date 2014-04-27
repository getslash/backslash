default: test

testserver: env
	.env/bin/python manage.py testserver

frontend: env
	gulp
.PHONY: frontend

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

env: .env/.up-to-date

.PHONY: env

.env/.up-to-date: base_requirements.txt flask_app/pip_requirements.txt Makefile package.json bower.json
	@echo "\x1b[32;01mSetting up environment. This could take a while...\x1b[0m"
	virtualenv .env
	.env/bin/pip install -r base_requirements.txt
	.env/bin/pip install -r flask_app/pip_requirements.txt
	.env/bin/pip install pytest flask-loopback requests
	npm install
	npm install -g gulp
	bower install
	touch .env/.up-to-date

deploy: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/production ansible/site.yml

deploy_staging: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/staging ansible/site.yml


deploy_localhost: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/localhost -c local --sudo ansible/site.yml

deploy_localhost_travis: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/localhost -c local --sudo ansible/site.yml
	.env/bin/python scripts/wait_for_travis.py

deploy_vagrant: env src_pkg.tar vagrant_up
	ANSIBLE_HOST_KEY_CHECKING=False .env/bin/ansible-playbook -i ansible/inventories/vagrant ansible/site.yml

vagrant_up:
	vagrant up
.PHONY: vagrant_up

src_pkg.tar:
	python scripts/build_tar.py
.PHONY: src_pkg.tar

test: env
	.env/bin/py.test tests/test_ut

travis_test: travis_system_install test deploy_localhost_travis
	.env/bin/py.test tests/ --www-port=80

travis_system_install:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev libevent-dev python-virtualenv

db_revision: env
	.env/bin/python manage.py db revision --autogenerate

db_migrate: env
	.env/bin/python manage.py db upgrade

