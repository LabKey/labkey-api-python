build:
	python -m build

release-test:
	hatch publish --repo test

release:
	hatch publish

install:
	pip install -e '.[dev,test]'

install-build:
    pip install -e '.[build]'

uninstall:
	pip uninstall -y labkey

clean:
	rm -rf ./dist/
	rm -rf ./labkey.egg-info

test-unit:
    pytest .

test-integration:
    pytest . -m "integration"

test: test-unit test-integration

brt: clean build release-test

br: clean build release
