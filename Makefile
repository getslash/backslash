default: test

testdb:
	pg_ctl init -D /tmp/pgsql -w
	pg_ctl start -D /tmp/pgsql -w
	createdb backslash
	.env/bin/python manage.py db upgrade

testserver:
	python manage.py testserver

clean:
	rm -rf .env webapp/tmp/ webapp/node_modules/ webapp/bower_components/ static
	find . -name "*.pyc" -delete

test:
	python manage.py unittest

webapp:
	python manage.py frontend build

.PHONY: webapp
