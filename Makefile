PKG_NAME := igcc
SRC := `find $(PKG_NAME)/ -name "*.py"`

clean:
	rm -rf build $(PKG_NAME).egg-info

lint:
	@uv tool run ruff check .

format:
	@uv tool run autoflake --in-place --remove-all-unused-imports $(SRC) \
		&& uv tool run isort $(SRC) \
		&& uv tool run black --line-length 100 $(SRC)

readme:
	@uv tool run mdup -i README.md

test:
	@for f in `ls tests`; do (cd tests/$$f && ./run.sh); done
