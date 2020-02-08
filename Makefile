

.PHONY: build-dist
build-dist:
	python setup.py sdist

.PHONY: upload-dist
upload-dist:
	twine upload dist/*

.PHONY: test
test:
	PYTHONPATH=`pwd` python3 -m pytest --cov=dynamof --cov-report term:skip-covered --cov-fail-under=100 --cov-report html test/unit/ -vv

.PHONY: lint
lint:
	pylint dynamof

.PHONY: check
check: lint test
	@echo "🎉 Check passed 👍"

.PHONY: fresh
fresh:
	python3 -m venv venv

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: travis
travis: check
	codeclimate-test-reporter
