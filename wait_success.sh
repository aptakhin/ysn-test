#!/bin/sh
#
# ./wait_success CONTAINER [CONTAINER...]
#
# Block until one or more containers stop. Print warning for every container with non-zero exit status.
#
# The wait_success utility exits 1 if any container have non-zero exit status, else 0.

set -e

exit_code=0

for container_name in "$@"; do
  container_exit_code=$(docker wait "$container_name")
  if [ "$container_exit_code" -ne 0 ]; then
    echo "Container $container_name stop with exit code $container_exit_code"
    exit_code=1
  fi
done

exit $exit_code
