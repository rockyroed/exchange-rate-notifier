.PHONY: lint format-fix format spell spell-fix typecheck

lint:
	flake8 .
	ruff check .

format-fix:
	black .
	isort .
	ruff check --fix .

format:
	black --check .
	isort --check-only .

spell-fix:
	codespell --write-changes .

spell:
	codespell .

typecheck:
	pyright .
