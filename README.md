The tiny webhook service for getting events from Appsflyer. Pythoned. Writes public and private data to Clickhouse.

# Prerequisites

```
docker with docker compose
make
```

# Commands

Run service with storage:

```bash
make run
```

Or manually the same:

```bash
docker compose up -d --build
```

Since logic is quite simple. I've used only integration tests:

```bash
make test
```

Run Flake8 linter:

```bash
make lint
```

Fast shortcut to lookup written data from ClickHouse:

```bash
make lookup-private
make lookup-public
```

Stop all and delete containers:

```bash
make clean
```

## Manual testing send

Send test data:

```bash
make run
curl -d @integration-test/templates/android.json "http://appsflyer_webhook_app:8400/attribution"
```

## Manual testing with Appsflyer

Send Appsflyer integration example from the site (need `ngrok` installed):

```bash
make run
ngrok http 8400
#
# `Send test` in Appsflyer to
# https://{NGROK_HOST}.ngrok.io/attribution
#
make lookup-private
```

### TODOs

- No shortcuts for fast local running on the machine. Only docker which is not fast when building
- No logger
- Some settings hardcoded in envs and docker-compose runs
- Add mypy
- In Clickhouse can add server-side buffer for faster inserting data
- In Clickhouse can try to optimize empty value strings
- No load testing code yet. `integration-test/templates/android.json` just a template to approach it.

### Open questions

- Now the public and private data don't have any joining column. Is it required to join somehow them?
