.PHONY: lint format check-format spell-check

lint:
	flake8 .

format:
	black .
	isort .

format-check:
	black --check .
	isort --check-only .

spell-fix:
	codespell --write-changes .

spell-check:
	codespell .
