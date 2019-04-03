default: test

testdb:
	pg_ctl init -D /tmp/pgsql -w
	pg_ctl start -D /tmp/pgsql -w
	createdb backslash
	pipenv run manage db upgrade

clean:
	rm -rf .env webapp/tmp/ webapp/node_modules/ static
	find . -name "*.pyc" -delete
