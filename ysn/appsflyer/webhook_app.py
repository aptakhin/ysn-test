import json
import logging
from http import HTTPStatus

from aiohttp import web

import appsflyer.settings as settings
from appsflyer.clickhouse_storage import (
    ClickhouseStorage,
    InvalidDataError,
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
        raise web.HTTPBadRequest(text='Expected json body')

    try:
        parsed = request.app['storage'].validate_insert(json_response)
    except InvalidDataError:
        raise web.HTTPBadRequest(
            text='Incorrect input, missing private fields',
        )

    try:
        await request.app['storage'].insert(parsed)
    except CantInsertToStorageError:
        raise web.HTTPInternalServerError(text="Can't write to storage")

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
        return await handler(request)
    except web.HTTPException:  # rethrow any HTTP code
        logging.exception('HTTP exception during execution')
        raise
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
