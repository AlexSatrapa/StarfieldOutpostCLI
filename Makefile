.DEFAULT_GOAL := dev-env
.PHONY: build package coverage test lint venv
PROJ_SLUG = outpostcli
CLI_NAME = outpost
PY_VERSION = 3.8
LINTER = pylint

dev-env: venv
	venv/bin/pip install --editable .

freeze: venv
	venv/bin/pip freeze > requirements.txt

lint:
	$(LINTER) $(PROJ_SLUG)

test: lint
	py.test --pyspec --cov-report term --cov=$(PROJ_SLUG) tests/

redgreen:
	fswatch -or outpostcli tests | xargs -n1 -I{} sh -c 'clear ; sleep 1 ; make test ;'

quicktest:
	py.test --pyspec --cov-report term --cov=$(PROJ_SLUG) tests/

coverage: lint
	py.test --cov-report html --cov=$(PROJ_SLUG) tests/

package: clean venv
	venv/bin/python setup.py sdist

clean:
	rm -rf dist \
	rm -rf *.egg-info
	coverage erase

venv: requirements.txt
	virtualenv --python python$(PY_VERSION) venv
	venv/bin/pip install -r requirements.txt

licenses: venv
	pip-licenses --with-url --format=rst \
	--ignore-packages $(shell cat .pip-lic-ignore | awk '{$$1=$$1};1')
