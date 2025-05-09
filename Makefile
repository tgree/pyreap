MODULE      := pyreap
MODULE_VERS := 0.9.2
MODULE_DEPS := \
		setup.cfg \
		setup.py \
		reap/*.py

FLAKE_MODULES := reap
LINT_MODULES  := reap

.PHONY: all
all: $(MODULE)

.PHONY: clean
clean:
	rm -rf dist psdb.egg-info build
	find . -name "*.pyc" | xargs rm
	find . -name __pycache__ | xargs rm -r

.PHONY: test
test: flake8 lint

.PHONY: flake8
flake8:
	python3 -m flake8 $(FLAKE_MODULES)

.PHONY: lint
lint:
	pylint $(LINT_MODULES)

.PHONY: $(MODULE)
$(MODULE): dist/$(MODULE)-$(MODULE_VERS)-py3-none-any.whl

.PHONY: install
install: $(MODULE)
	sudo pip3 uninstall -y $(MODULE) --break-system-packages
	sudo pip3 install dist/$(MODULE)-$(MODULE_VERS)-py3-none-any.whl --break-system-packages

.PHONY: uninstall
uninstall:
	sudo pip3 uninstall $(MODULE)

dist/$(MODULE)-$(MODULE_VERS)-py3-none-any.whl: $(MODULE_DEPS) Makefile
	python3 setup.py --quiet sdist bdist_wheel
	python3 -m twine check $@
