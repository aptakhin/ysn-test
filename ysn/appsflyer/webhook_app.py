import json
import logging
from http import HTTPStatus

from aiohttp import web

import appsflyer.settings as settings
from appsflyer.clickhouse_storage import (
    ClickhouseStorage,
    CantInsertToStorageError,
)

#
# TODO: logging configuration
#
logger = logging.getLogger(__name__)


#
# TODO: init Sentry
#

async def index(request):
    return web.Response(text='Appsflyer webhook')


async def attribution(request):
    try:
        json_response = await request.json()
    except json.decoder.JSONDecodeError:
        logger.exception("Expected missing json body")

    # TODO 1: We need here some proper validation with pydantic
    # TODO 2: We need here some fast broker like Redis/RabbitMQ for rounded
    #         and batched inserts to Clickhouse

    try:
        await request.app['storage'].insert(json_response)
    except CantInsertToStorageError:
        logger.exception("Can't write to storage")

    return web.Response(text='')


async def storage(app):
    app['storage'] = ClickhouseStorage(
        settings.CLICKHOUSE_HTTP_URL,
    )
    yield
    await app['storage'].close()


@web.middleware
async def catch_uncought_exception(request, handler):
    try:
        resp = await handler(request)
        return resp
    except:  # noqa: E722
        logger.exception('Caught unhandled exception')
        return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR.value)


async def webhook_app():
    app = web.Application(
        middlewares=[
            catch_uncought_exception,
        ],
    )
    app.router.add_get('/', index)
    app.router.add_post('/attribution', attribution)
    app.cleanup_ctx.append(storage)
    return app
