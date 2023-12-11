# Makefile for setting up Advent of Code challenges

# Variables
THIS_YEAR := $(shell date +%Y)
DAY_DIR := day$(DAY)
CHALLENGE_FILENAME := challenge.py
INPUT_FILENAME := puzzle_input.txt
TEMPLATE_FILENAME := template.py

# Default target
all: setup_files

# Setup directory structure
.PHONY: setup_dir
setup_dir:
	mkdir -p $(THIS_YEAR)/$(DAY_DIR)

# Setup challenge and input files from a template
.PHONY: setup_files
setup_files: setup_dir
	if [ ! -f $(THIS_YEAR)/$(DAY_DIR)/$(CHALLENGE_FILENAME) ]; then \
		cp $(TEMPLATE_FILENAME) $(THIS_YEAR)/$(DAY_DIR)/$(CHALLENGE_FILENAME); \
	fi
	touch $(THIS_YEAR)/$(DAY_DIR)/$(INPUT_FILENAME)

# Clean up generated files and directories
.PHONY: clean
clean:
	rm -rf $(THIS_YEAR)/$(DAY_DIR)
