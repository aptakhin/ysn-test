import asyncio
import json
from typing import Any, Dict

from aiohttp import ClientSession, web


async def _get_first_json_row(response: web.Request) -> Dict[str, Any]:
    """Clickhouse-HTTP helper for getting data from JSON"""
    raw_response = await response.text()
    lines = raw_response.split('\n')
    load = lines[0]
    return json.loads(load)


async def test_insert_android():
    async with ClientSession() as session:
        await session.post(
            'http://appsflyer_webhook_app:8400/attribution',
            data=open('templates/android.json').read(),
        )

        # TODO: in our case it's okay, but need some faster cycle check
        await asyncio.sleep(2)

        private_resp = await session.get(
            'http://clickhouse-server:8123/?query=SELECT * FROM default.private_hits FORMAT JSONEachRow',
        )
        private_resp_json = await _get_first_json_row(private_resp)
        assert private_resp_json['idfa'] == 'A7071198-3848-40A5-B3D0-94578D9BZZZZ'
        # TODO: check other fields

        public_resp = await session.get(
            'http://clickhouse-server:8123/?query=SELECT * FROM default.public_hits FORMAT JSONEachRow',
        )
        public_resp_json_row = await _get_first_json_row(public_resp)
        # In public_data json_data encoded again in json
        public_resp_json = json.loads(public_resp_json_row['json_data'])

        PRIVATE_COLUMNS = ('idfa', 'idfv', 'advertising_id', 'android_id')
        print(public_resp_json, type(public_resp_json))
        assert all(column not in public_resp_json for column in PRIVATE_COLUMNS)
        assert public_resp_json['event_time_selected_timezone'] == '2020-01-15 14:57:24.898+0000'
        # TODO: check other fields and compare wih file
