default: test

clean:
	rm -rf .env .ansible-env
	find . -name "*.pyc" -delete

test:
	python manage.py unittest
