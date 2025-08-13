.PHONY: lint-and-format

lint-and-format:
	flake8 .
	black --check .
	isort --check-only .
	codespell .

lint-and-format-fix:
	black .
	isort .
	codespell --write-changes .