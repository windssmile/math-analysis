.PHONY: test check generate render verify preview

PYTHON ?= python3.12

test:
	$(PYTHON) -m unittest discover -s tests -v

check:
	$(PYTHON) scripts/check_outline.py
	$(PYTHON) scripts/check_units.py

generate:
	$(PYTHON) scripts/render_curriculum_map.py

render: generate
	quarto render

verify: test check render
	$(PYTHON) scripts/check_site.py

preview: generate
	quarto preview
