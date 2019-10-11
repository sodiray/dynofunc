

.PHONY: build-distribution
build-dist:
	python setup.py sdist

.PHONY: upload-dist
upload-dist:
	twine upload dist/*

.PHONY: test
test:
	PYTHONPATH=`pwd` python3 -m pytest --cov=dynamof --cov-report term:skip-covered --cov-fail-under=100 test/

.PHONY: lint
lint:
	pylint biscuit

.PHONY: fresh
fresh:
	python3 -m venv venv
	pip install -r requirements.txt
