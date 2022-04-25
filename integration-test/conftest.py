from aiohttp import ClientSession

import pytest


@pytest.fixture(scope='function')
async def client_session():
    """Manages HTTP-session for tests."""
    async with ClientSession(raise_for_status=True) as session:
        yield session
