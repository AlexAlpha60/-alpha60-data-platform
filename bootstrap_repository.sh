#!/bin/bash
set -e

mkdir -p \
  docs/architecture/decisions \
  docs/operations/runbooks \
  docs/standards \
  src/alpha60/config \
  src/alpha60/core \
  src/alpha60/connectors/shopify \
  src/alpha60/warehouse \
  src/alpha60/jobs \
  sql/raw/shopify \
  sql/staging/shopify \
  sql/marts/inventory \
  sql/tests \
  infra/cloud-run \
  infra/scheduler \
  infra/bigquery/tables \
  infra/secrets \
  tests/unit \
  tests/integration \
  tests/fixtures \
  scripts \
  .github/workflows

touch \
  src/alpha60/__init__.py \
  src/alpha60/config/__init__.py \
  src/alpha60/core/__init__.py \
  src/alpha60/connectors/__init__.py \
  src/alpha60/connectors/shopify/__init__.py \
  src/alpha60/warehouse/__init__.py \
  src/alpha60/jobs/__init__.py

cat > README.md <<'README'
# ALPHA60 Data Platform

Production-grade operational data platform for ALPHA60.

The first implementation focus is Shopify inventory ingestion into BigQuery.

## Project Structure

- `src/alpha60/` - Python application code
- `sql/` - BigQuery SQL models and checks
- `infra/` - Cloud infrastructure configuration
- `tests/` - automated tests
- `docs/` - architecture, standards, and operations documentation
- `scripts/` - developer and deployment helper scripts
README

cat > .gitignore <<'GITIGNORE'
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.DS_Store
dist/
build/
*.egg-info/
GITIGNORE

cat > .env.example <<'ENV'
# Google Cloud
GOOGLE_CLOUD_PROJECT=alpha60-data-platform
BIGQUERY_LOCATION=australia-southeast1

# Shopify
SHOPIFY_SHOP_NAME=
SHOPIFY_ACCESS_TOKEN=

# Runtime
ENVIRONMENT=local
LOG_LEVEL=INFO
ENV

cat > pyproject.toml <<'PYPROJECT'
[project]
name = "alpha60-data-platform"
version = "0.1.0"
description = "ALPHA60 operational data platform"
requires-python = ">=3.13,<3.14"

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
PYPROJECT

cat > requirements.txt <<'REQ'
google-cloud-bigquery
google-cloud-secret-manager
requests
pydantic
pydantic-settings
REQ

cat > requirements-dev.txt <<'REQDEV'
pytest
ruff
mypy
REQDEV

cat > Makefile <<'MAKE'
.PHONY: install test lint format

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff check src tests

format:
	. .venv/bin/activate && ruff format src tests
MAKE

cat > docs/architecture/overview.md <<'DOC'
# Architecture Overview

The ALPHA60 Data Platform is designed as a production-grade operational data platform.

Initial scope:
- Shopify inventory extraction
- BigQuery raw storage
- staged modelling
- operational reporting foundations
DOC

cat > docs/architecture/decisions/adr-0001-project-structure.md <<'ADR'
# ADR-0001: Project Structure

## Status

Accepted

## Decision

The repository separates application code, SQL, infrastructure, tests, scripts, and documentation.

## Rationale

This structure supports long-term maintainability and keeps each concern clearly owned.
ADR

git init
git add .
git commit -m "Initial ALPHA60 data platform scaffold"

echo "Repository bootstrap complete."
