build_dev:
	cp -r build_data/configurations/dev/. .
	docker-compose build

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

