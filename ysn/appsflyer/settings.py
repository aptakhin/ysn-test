import os

#
# Just example how it is cool with environment variables passed to containers
#

CLICKHOUSE_HTTP_URL = os.getenv('YSN_APPSFLYER_WEBHOOK_CLICKHOUSE_HTTP_URL')
