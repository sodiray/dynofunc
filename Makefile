

.PHONY: build-distribution
build-distribution:
	@echo "building..."

.PHONY: test
test:
	PYTHONPATH=`pwd` pytest --cov=idynamo --cov-report term:skip-covered --cov-fail-under=100 test/

.PHONY: lint
lint:
	pylint biscuit
