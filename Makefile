include .env
export

# enumeration of * .py files storage or folders is required.
files_to_check 	?= app tests

## Git pull command
pull:
	git pull

## Check code quality
check: ruff mypy

## Check pep8
ruff:
	ruff check ${files_to_check} --fix

## Check typing
mypy:
	mypy ${files_to_check}

test:
	pytest tests/
