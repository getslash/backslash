default: test

testdb:
	pg_ctl init -D /tmp/pgsql -w
	pg_ctl start -D /tmp/pgsql -w
	createdb backslash
	.env/bin/python manage.py db upgrade

testserver:
	.env/bin/python manage.py testserver

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

test:
	python manage.py unittest

travis-test:
	python manage.py travis-test

webapp:
	python manage.py frontend build

.PHONY: webapp
