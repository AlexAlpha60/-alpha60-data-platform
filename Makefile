.PHONY: install test lint typecheck format quality

install:
	uv sync --dev

test:
	uv run pytest

lint:
	uv run ruff check src tests

typecheck:
	uv run mypy src tests

format:
	uv run ruff format src tests

quality: lint typecheck test