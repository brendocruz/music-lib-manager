SHELL := /bin/bash

VIRTUAL_ENVIRONMENT = .venv
ACTIVATE_SCRIPT     = $(VIRTUAL_ENVIRONMENT)/bin/activate
REQUIREMENTS_FILE   = requirements.txt

TARGET ?= "john.json"

setup:
	@python3 -m venv $(VIRTUAL_ENVIRONMENT)
	@test -f $(REQUIREMENTS_FILE) && \
		source $(ACTIVATE_SCRIPT) && \
		pip install -r $(REQUIREMENTS_FILE) || \
		exit 0

add-package:
	@source $(ACTIVATE_SCRIPT) && \
		read -p "Package name: " PACKAGE && \
		pip install $${PACKAGE}

remove-package:
	@source $(ACTIVATE_SCRIPT) && \
		read -p "Package name: " PACKAGE && \
		pip uninstall $${PACKAGE}

freeze:
	@source $(ACTIVATE_SCRIPT) && \
		pip freeze > $(REQUIREMENTS_FILE)

download:
	@source $(ACTIVATE_SCRIPT) && \
		python3 download.py $(TARGET)


.PHONY: setup add-package remove-package freeze 
