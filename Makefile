upload:
	rm -rf dist
	python setup.py sdist
	twine upload dist/covid-ru-*.tar.gz
