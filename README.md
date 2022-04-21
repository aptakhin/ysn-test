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

Since logic is quite simple. I've used only integration tests:

```bash
make test
```

Run Flake8 linter:

```bash
make lint
```

Fast shortcut to lookup writen data:

```bash
make lookup-private
make lookup-public
```

Stop all and delete data:

```bash
make clean
```

### TODOs:
- No shortcuts for fast local running on machine. Only docker which is not fast when building
- No logger
- Some settings hardcoded in envs and docker-compose runs
- Add mypy