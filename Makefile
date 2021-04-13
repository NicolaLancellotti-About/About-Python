PYTHON=venv/bin/python3

# ______________________________________________________________________________

.SILENT:
.NOTPARALLEL:

.PHONY: help - Lists targets.
help:
	echo "Targets:"
	sed -nr 's/^.PHONY: (.*) - (.*)/\1|\2/p' ${MAKEFILE_LIST} | \
		awk -F '|' '{printf "* %-30s %s\n", $$1, $$2}' | sort

# ____________________________________________________________________________________________________
# All

.PHONY: all - All.
all:	venv-create \
		format \
		lint \
		test \
		run

# ____________________________________________________________________________________________________
# Python Virtual Environment

.PHONY: venv-create - Create Virtual Environment.
venv-create:
	python3 -m venv venv
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install -r requirements.txt

# ____________________________________________________________________________________________________
# Format

.PHONY: format - Format.
format:
	${PYTHON} -m black about_python tests
	${PYTHON} -m isort about_python tests --profile black

# ____________________________________________________________________________________________________
# Lint

.PHONY: lint - Lint.
lint:
	${PYTHON} -m pyright --pythonpath=${PYTHON}

# ____________________________________________________________________________________________________
# Test

.PHONY: test - Test.
test:
	${PYTHON} -m pytest tests

# ____________________________________________________________________________________________________
# Run

.PHONY: run - Run.
run:
	${PYTHON} -m about_python
