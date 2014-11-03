default: test

testserver:
	.env/bin/python manage.py testserver

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

test: webapp
	python manage.py unittest

webapp:
	.env/bin/python manage.py frontend build

.PHONY: webapp
