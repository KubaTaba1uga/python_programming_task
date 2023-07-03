services := app upstream

help:
	@echo "build - build docker images"
	@echo "run - run docker images"
	@echo "tests - run tests quickly with pytest"


build:
	sudo docker-compose build $(services)

run:
	sudo docker-compose up

test:
	sudo docker-compose up -d
	python -m pytest -vv
	sudo docker-compose down
