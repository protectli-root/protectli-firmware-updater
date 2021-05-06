all: build dist share

dist:
	@mkdir dist/
	@tar -czf dist/flashli.tar.gz build/*
	@echo 'Distributable tarball at ./dist/flashli.tar.gz'

build:
	@mkdir build/
	@cp -r flashli/ images/ vendor/ flashbios README.md build/
	@echo 'Application and sources built into ./build/'

share:
	@mkdir share/
	@cp -r flashli/ images/ vendor/ dist/ flashbios README.md share/
	@echo 'Shareable GitHub config built into ./share/'

.PHONY: clean
clean:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf share/
