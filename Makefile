.PHONY: help clean build_eggs build

help:
	@echo -e "  \033[0;36mhelp\033[0m         - print this message"
	@echo -e "  \033[0;36mclean\033[0m        - remove artifacts"
	@echo -e "  \033[0;36mpackage\033[0m      - package submittable artifacts"
	@echo -e "  \033[0;36mbuild\033[0m        - clean -> lint -> test -> package"

clean:
	@echo -e "\033[0;36mClean\033[0m"
	rm -rf .mypy_cache/ .pytest_cache/ htmlcov/ .coverage
	rm -rf build/ dist/
	find . -name '*.pyc' -exec rm -rf {} +

build:
	@echo -e "\033[0;36mBuild Eggs\033[0m"
	isort src
	black --skip-string-normalization --line-length=100 src
	flake8 src
	pylint src


build: clean build