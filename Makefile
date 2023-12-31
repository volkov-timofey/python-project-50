#Makefile

install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml

gendiff: # run gendiff
	poetry run gendiff

build: # build project
	poetry build

publish: # publish without PyPI
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

lint: # run_linter
	poetry run flake8 gendiff
	
full: build publish package-install

check: test lint

selfcheck:
	check