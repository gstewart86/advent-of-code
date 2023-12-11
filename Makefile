# Makefile for Advent of Code challenge setup and execution

YEAR := $(shell date +%Y)
LAST_DAY := $(shell ls $(YEAR)/day* -d 2>/dev/null | sort | tail -n1 | grep -oP 'day\K[0-9]+' || echo 0)
NEXT_DAY := $(shell echo $$(( $(LAST_DAY) + 1 )) )
DAY ?= $(LAST_DAY)
DAY_ARG := $(DAY)
CHALLENGE_FILENAME := challenge.py
INPUT_FILENAME := puzzle_input.txt
TEMPLATE_FILENAME := template.py
VENV_DIR := .venv

# Create a new day's challenge
.PHONY: new
new:
	$(eval DAY_ARG := $(if $(DAY),$(DAY),$(NEXT_DAY)))
	mkdir -p $(YEAR)/day$(DAY_ARG)
	if [ ! -f $(YEAR)/day$(DAY_ARG)/$(CHALLENGE_FILENAME) ]; then \
		cp $(TEMPLATE_FILENAME) $(YEAR)/day$(DAY_ARG)/$(CHALLENGE_FILENAME); \
	fi
	touch $(YEAR)/day$(DAY_ARG)/$(INPUT_FILENAME)

# Setup workspace (virtual environment and requirements)
.PHONY: setup
setup:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Run the challenge for a specified day using the Python script
.PHONY: run
run:
	python tools/run_challenge.py --day $(DAY) --year $(YEAR)

# Clean up generated files and directories
.PHONY: clean
clean:
	rm -rf $(YEAR)/day$(DAY)
