.PHONY: test check generate render verify preview

test:
	python3 -m unittest discover -s tests -v

check:
	python3 scripts/check_outline.py
	python3 scripts/check_units.py

generate:
	python3 scripts/render_curriculum_map.py

render: generate
	quarto render

verify: test check render
	python3 scripts/check_site.py

preview: generate
	quarto preview
