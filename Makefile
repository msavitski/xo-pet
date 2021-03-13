ifneq (,$(wildcard ./.env))
    include .env
    include secrets.env
    export
endif

build_dev:
	cp -r build_data/configurations/dev/. .
	docker-compose build

first_deploy_dev: build_dev
	docker-compose up -d
	cd src/db && alembic revision --autogenerate -m 'Commit' && alembic upgrade head

deploy_dev:
	cp -r build_data/configurations/dev/. .
	docker-compose up -d --build

logs:
	docker-compose logs -f

reload:
	docker-compose up -d

kill:
	docker-compose kill

ps:
	docker-compose ps

