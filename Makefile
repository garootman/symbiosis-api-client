.PHONY: lint format typecheck security check-all docs html clean test build publish

lint:
	pre-commit run ruff --all-files

format:
	pre-commit run black --all-files

typecheck:
	pre-commit run mypy --all-files

security:
	pre-commit run bandit --all-files

check-all:
	pre-commit run --all-files

docs:
	sphinx-build -b html docs/ docs/_build

# Open the generated HTML documentation in a web browser
html: docs
	open docs/_build/index.html

# Clean up build artifacts
clean:
	rm -rf dist/ docs/_build/ *.egg-info

# Run tests using pytest
test:
	PYTHONPATH=src pytest

build:
	uv build

publish:
	uv publish

tox:
	tox -e py39,py310,py311,py312,py313,lint
