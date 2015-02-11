default: test

testserver:
	python manage.py testserver

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

test:
	python manage.py unittest

webapp:
	python manage.py frontend build

.PHONY: webapp
