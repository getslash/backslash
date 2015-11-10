default: test

testserver:
	python manage.py testserver

clean:
	rm -rf .env .ansible-env webapp/tmp/ webapp/node_modules/ webapp/bower_components/ static
	find . -name "*.pyc" -delete

test:
	python manage.py unittest

webapp:
	python manage.py frontend build

.PHONY: webapp
