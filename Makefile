.PHONY: help

help:  ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
setup:  ## Initialize project dev dependencies
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install
	pre-commit install
lockdeps:  ## Update poetry.lock
	poetry lock
format:  ## Format python files
	poetry run black .
	poetry run isort .
test:  ## Run tests
	poetry run pytest
coverage:  ## Run coverage report
	poetry run coverage run
	poetry run coverage report
