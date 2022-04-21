from dataclasses import dataclass
import json
from typing import Any, Dict

from aiohttp import ClientSession, ClientError
from aiochclient import ChClient


class CantInsertToStorageError(RuntimeError):
    pass


@dataclass
class PublicPrivateHits:
    public: Dict[str, Any]
    private: Dict[str, Any]

    PRIVATE_FIELDS = ('idfa', 'idfv', 'advertising_id', 'android_id')

    @classmethod
    def split(cls, json_data: Dict[str, Any]) -> 'PublicPrivateHits':
        public_data = json_data.copy()  # Only copy keys
        private_data = {
            item: public_data.pop(item)
            for item in cls.PRIVATE_FIELDS
        }
        return PublicPrivateHits(public=public_data, private=private_data)


class ClickhouseStorage:
    def __init__(self, clickhouse_http_url: str):
        self._client = ChClient(
            session=ClientSession(),
            url=clickhouse_http_url,
        )

    async def insert(self, json_data: Dict[str, Any]) -> None:
        parsed = PublicPrivateHits.split(json_data)
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

    @staticmethod
    def _split_public_and_private_hits(json_data: Dict[str, Any]) \
            -> PublicPrivateHits:
        public_data = json_data.copy()  # Only copy keys
        private_data = {
            item: public_data.pop(item)
            for item in PublicPrivateHits.PRIVATE_FIELDS
        }
        return PublicPrivateHits(public=public_data, private=private_data)
