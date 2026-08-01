PYTHON = python3
MAP = maps/medium/01_dead_end_trap.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py $(MAP)

debug:
	# Run in debug mode using Python's built-in pdb[cite: 1]
	$(PYTHON) -m pdb main.py $(MAP)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy --strict .