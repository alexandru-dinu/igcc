PKG_NAME := igcc
SRC := `find $(PKG_NAME)/ -name "*.py"`

clean:
	rm -rf build $(PKG_NAME).egg-info

lint:
	@ruff check .

format:
	@autoflake --in-place --remove-all-unused-imports $(SRC) \
		&& isort $(SRC) \
		&& black --line-length 100 $(SRC)

test:
	@for f in `ls tests`; do (cd tests/$$f && ./run.sh); done