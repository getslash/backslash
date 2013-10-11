testserver: .env
	.env/bin/python manage.py testserver

.env/.up-to-date: base_requirements.txt flask_app/pip_requirements.txt
	virtualenv .env
	.env/bin/pip install -r base_requirements.txt
	.env/bin/pip install -r flask_app/pip_requirements.txt
	touch .env/.up-to-date

deploy: src_pkg.tar
	python scripts/deploy $(target)

local_deploy: src_pkg.tar
	python scripts/deploy --sudo localhost

src_pkg.tar:
	python scripts/build_tar.py

.PHONY: src_pkg.tar

travis_install:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev libevent-dev
	pip install --use-mirrors -r base_requirements.txt
	make local_deploy

travis_test: .env/.up-to-date
	.env/bin/pip install nose
	.env/bin/nosetests -w tests --tc www_port:80
