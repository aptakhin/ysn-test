from dataclasses import dataclass
import json
from typing import Any, Dict

from aiohttp import ClientSession
from aiochclient import ChClient, ChClientError


class InvalidDataError(ValueError):
    pass


class CantInsertToStorageError(RuntimeError):
    pass


@dataclass
class PublicPrivateHits:
    """Helper dataclass to divide public and private fields."""
    public: Dict[str, Any]
    private: Dict[str, Any]

    PRIVATE_FIELDS = ('idfa', 'idfv', 'advertising_id', 'android_id')

    @classmethod
    def split(cls, json_data: Dict[str, Any]) -> 'PublicPrivateHits':
        """Splits the given json data to public and private classes"""
        # TODO: Need unit-tests
        public_data = json_data.copy()  # Only copy keys
        try:
            private_data = {
                item: public_data.pop(item)
                for item in cls.PRIVATE_FIELDS
            }
        except KeyError as e:
            raise InvalidDataError(f'Missing field {e}')
        return PublicPrivateHits(public=public_data, private=private_data)


class ClickhouseStorage:
    """Storage class for insert interface for app."""
    def __init__(self, clickhouse_http_url: str):
        self._client = ChClient(
            session=ClientSession(),
            url=clickhouse_http_url,
        )

    def validate_insert(self, json_data: Dict[str, Any]) -> PublicPrivateHits:
        return PublicPrivateHits.split(json_data)

    async def insert(self, parsed: PublicPrivateHits) -> None:
        """Insert the data from Appsflyer."""

        # TODO 1: We need here some proper validation with pydantic
        # TODO 2: We need here some fast broker like Redis/RabbitMQ for rounded
        #         and batched inserts to Clickhouse
        # TODO 3: Here can parallel insert queries

        await self._insert(
            'INSERT INTO default.private_hits FORMAT JSONEachRow',
            parsed.private,
        )

        await self._insert(
            'INSERT INTO default.public_hits FORMAT JSONEachRow',
            {'json_data': json.dumps(parsed.public)},
        )

    async def close(self) -> None:
        await self._client.close()

    async def _insert(self, query, *args) -> None:
        try:
            await self._client.execute(query, args)
        except ChClientError as e:
            raise CantInsertToStorageError() from e
