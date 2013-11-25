default: test

testserver: env
	.env/bin/python manage.py testserver

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

env: .env/.up-to-date

.PHONY: env

.env/.up-to-date: base_requirements.txt flask_app/pip_requirements.txt
	virtualenv .env
	.env/bin/pip install -r base_requirements.txt
	.env/bin/pip install -r flask_app/pip_requirements.txt
	.env/bin/pip install nose
	touch .env/.up-to-date

deploy: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/production ansible/site.yml

deploy_staging: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/staging ansible/site.yml


deploy_localhost: src_pkg.tar env
	.env/bin/ansible-playbook -i ansible/inventories/localhost -c local --sudo ansible/site.yml

deploy_localhost_travis: deploy_localhost
	sleep 5 # travis uses slow nodes and tends to take time to bring the uwsgi app online

deploy_vagrant: src_pkg.tar vagrant_up
	ansible-playbook -i ansible/inventories/vagrant ansible/site.yml

vagrant_up:
	vagrant up
.PHONY: vagrant_up

src_pkg.tar:
	python scripts/build_tar.py
.PHONY: src_pkg.tar

test: env
	.env/bin/nosetests tests/test_ut

travis_test: travis_system_install test deploy_localhost_travis
	.env/bin/nosetests tests/test_deployment --tc www_port:80

travis_system_install:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev libevent-dev python-virtualenv
