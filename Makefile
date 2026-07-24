.PHONY: test check build verify preview

PYTHON ?= python3.12

test:
	$(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) scripts/check_content.py

build: check
	mkdocs build --strict

site-check: build
	$(PYTHON) scripts/check_site.py

verify: test check build site-check

preview:
	mkdocs serve
