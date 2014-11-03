default: test

testserver:
	.env/bin/python manage.py testserver

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

test: webapp
	python manage.py unittest

travis-test: webapp
	python manage.py travis-test

webapp:
	python manage.py frontend build

.PHONY: webapp
