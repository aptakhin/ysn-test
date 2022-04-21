clean:
	docker compose -f docker-compose.yaml -f docker-compose-integration-test.yaml stop
	docker compose -f docker-compose.yaml -f docker-compose-integration-test.yaml rm --force

run: clean
	docker compose up -d --build

test: clean
	docker compose -f docker-compose.yaml -f docker-compose-integration-test.yaml up -d --build
	docker logs -f ysn_appsflyer_webhook_app_integration_test
	./wait_success.sh ysn_appsflyer_webhook_app_integration_test

lint: run
	docker compose exec appsflyer_webhook_app flake8

lookup-private:
	docker exec ysn_appsflyer_clickhouse_server clickhouse client -q 'SELECT * FROM default.private_hits FORMAT PrettyCompact'

lookup-public:
	docker exec ysn_appsflyer_clickhouse_server clickhouse client -q 'SELECT * FROM default.public_hits FORMAT PrettyCompact'
