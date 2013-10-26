testserver: .env
	.env/bin/python manage.py testserver

.env/.up-to-date: base_requirements.txt flask_app/pip_requirements.txt
	virtualenv .env
	.env/bin/pip install -r base_requirements.txt
	.env/bin/pip install -r flask_app/pip_requirements.txt
	touch .env/.up-to-date

deploy: src_pkg.tar .env/.up-to-date
	.env/bin/ansible-playbook -i ansible/inventories/production ansible/site.yml

deploy_staging: src_pkg.tar .env/.up-to-date
	.env/bin/ansible-playbook -i ansible/inventories/staging ansible/site.yml


deploy_localhost: src_pkg.tar .env/.up-to-date
	.env/bin/ansible-playbook -i ansible/inventories/localhost -c local --sudo ansible/site.yml

deploy_vagrant: vagrant_up
	ansible-playbook -i ansible/inventories/vagrant ansible/site.yml

vagrant_up:
	vagrant up
.PHONY: vagrant_up

src_pkg.tar:
	python scripts/build_tar.py
.PHONY: src_pkg.tar

travis_test: travis_system_install deploy_localhost
	.env/bin/pip install nose
	sleep 5 # travis uses slow nodes and tends to take time to bring the uwsgi app online
	.env/bin/nosetests -w tests --tc www_port:80

travis_system_install:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev libevent-dev python-virtualenv


