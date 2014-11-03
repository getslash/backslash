default: test

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
