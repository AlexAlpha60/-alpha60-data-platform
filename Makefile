.PHONY: install test lint format

install:
	uv sync --dev

test:
	uv run pytest

lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests