sources := src tests upstream
services := app upstream

help:
	@echo "lint - check style with ruff and mypy"
	@echo "format - format style with black and isort"
	@echo "install - install requirements"
	@echo "install-dev - install dev requirements"
	@echo "tests - run tests quickly with pytest"
	@echo "build - build docker images"
	@echo "run - run docker images"

lint:
	python -m ruff $(sources)
	python -m mypy $(sources)

format:
	python -m black $(sources)
	python -m isort $(sources)

install: 
	pip install .

install-dev: 
	pip install -e .[dev]

test:
	sudo docker-compose up -d
	python -m pytest -vv
	sudo docker-compose down

build:
	sudo docker-compose build $(services)

run:
	sudo docker-compose up
