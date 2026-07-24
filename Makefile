.PHONY: test check build verify preview

PYTHON ?= python3.12

test:
	$(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) scripts/check_content.py

build: check
	mkdocs build --strict

verify: test build

	mkdocs serve
