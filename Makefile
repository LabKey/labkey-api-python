.PHONY: build
build:
	python -m build

.PHONY: release-test
release-test:
	twine upload dist/* -r testpypi

.PHONY: release
release:
	twine upload dist/* -r pypi

.PHONY: install
install:
	pip install -e '.[dev,build]'

.PHONY: uninstall
uninstall:
	pip uninstall -y labkey

.PHONY: clean
clean:
	rm -rf ./dist/
	rm -rf ./labkey.egg-info