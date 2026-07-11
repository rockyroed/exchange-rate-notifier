.PHONY: lint lint-and-format lint-and-format-fix format-fix format spell spell-fix typecheck

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

lint-and-format:
	flake8 .
	ruff check .
	black --check .
	isort --check-only .
	codespell .

lint-and-format-fix:
	flake8 .
	ruff check .
	black .
	isort .
	codespell --write-changes .	

typecheck:
	pyright .
