default: test

testserver:
	python manage.py testserver

clean:
	rm -rf .env .ansible-env
	find . -name "*.pyc" -delete

test:
	python manage.py unittest
