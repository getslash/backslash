default: test

clean:
	rm -rf .env
	find . -name "*.pyc" -delete

test:
	python manage.py unittest
