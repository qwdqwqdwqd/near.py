import asyncio
import atexit
from json import JSONDecodeError
from typing import Any, Type

import requests
from aiohttp import ClientSession

from near.exceptions import BadResponseError
from near.providers.base import BaseAsyncJSONProvider, BaseSyncJSONProvider
from near.types import RPC, ResultSchemaT, RPCEndpoint


class HTTPProvider(BaseSyncJSONProvider):
    def __init__(self, endpoint_uri: str, timeout: int) -> None:
        self.endpoint_uri = endpoint_uri
        self.timeout = timeout
        super().__init__()

    def post(self, method: RPCEndpoint, params: Any) -> dict:
        payload = self.encode_rpc_request(method, params)
        response = requests.post(self.endpoint_uri, json=payload, timeout=self.timeout)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise BadResponseError("Couldn't decode the response into json")

    def call_rpc(
        self, method: RPCEndpoint, params: Any, result_schema: Type[ResultSchemaT]
    ) -> ResultSchemaT:
        response_dict = self.post(method, params)
        return self.get_result(response_dict, result_schema)

    def is_connected(self) -> bool:
        result = self.post(RPC.status, [])
        return "result" in result


class AsyncHTTPProvider(BaseAsyncJSONProvider):
    def __init__(self, endpoint_uri: str, timeout) -> None:
        self.endpoint_uri: str = endpoint_uri
        self.timeout = timeout
        self._session = None
        atexit.register(self._shutdown)
        super().__init__()

    @property
    def session(self):
        if not self._session:
            self._session = ClientSession()

        return self._session

    def _shutdown(self):
        if self._session:
            asyncio.run(self.session.close())

    async def post(self, method: RPCEndpoint, params: Any) -> dict:
        payload = self.encode_rpc_request(method, params)
        async with self.session.post(
            self.endpoint_uri,
            json=payload,
            timeout=self.timeout,
        ) as response:
            try:
                return await response.json(content_type=None)
            except JSONDecodeError:
                raise BadResponseError("Couldn't decode the response into json")

    async def call_rpc(
        self, method: RPCEndpoint, params: Any, result_schema: Type[ResultSchemaT]
    ) -> ResultSchemaT:
        response_dict = await self.post(method, params)
        return self.get_result(response_dict, result_schema)

    async def is_connected(self) -> bool:
        result = await self.post(RPC.status, [])
        return "result" in result
