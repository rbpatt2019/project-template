VERSION=$$(grep version pyproject.toml | sed -n 1p | awk '/version/ {print $$3}' | tr -d '"' | awk '{print "v"$$0}')

define tags
git add pyproject.toml
git commit -m "VERSION bump"
git tag $(VERSION)
git push origin master --tags
endef

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	rm -rf html/
	rm -rf doctrees/

update:
	poetry update
	poetry run pre-commit autoupdate
	git add poetry.lock .pre-commit-config.yaml
	git commit -m 'Update dependencies'

develop:
	poetry install

install:
	poetry install --no-dev

format: clean
	poetry run nox -s form

lint: format
	poetry run nox -s lint type
	poetry check

test: clean
	poetry run nox -s tests security

patch: lint test
	poetry run nox -s doc_tests doc_build
	$(tags)

minor: lint test
	poetry run nox -s doc_tests doc_build
	$(tags)

major: lint test
	poetry run nox -s doc_tests doc_build
	$(tags)

dist: clean
	poetry build

release: dist
	poetry publish

.PHONY: clean reqs update develop install format lint test patch minor major dist release
