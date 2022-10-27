import asyncio
import atexit
from json import JSONDecodeError
from typing import Any, cast

import requests
from aiohttp import ClientSession

from near.constants import DEFAULT_TIMEOUT
from near.exceptions import BadResponseError
from near.providers.base import BaseAsyncJSONProvider, BaseSyncJSONProvider
from near.types import RPC, RPCEndpoint, RPCResponse


class HTTPProvider(BaseSyncJSONProvider):
    def __init__(self, endpoint_uri: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.endpoint_uri = endpoint_uri
        self.timeout = timeout
        super().__init__()

    def post(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        payload = self.encode_rpc_request(method, params)
        response = requests.post(self.endpoint_uri, json=payload, timeout=self.timeout)
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            raise BadResponseError("Couldn't decode the response into json")

        result = cast(RPCResponse, response_json)
        self.handle_response(result)
        return result

    def is_connected(self) -> bool:
        result = self.post(RPC.status, [])
        return "result" in result


class AsyncHTTPProvider(BaseAsyncJSONProvider):
    def __init__(self, endpoint_uri: str, timeout: int = DEFAULT_TIMEOUT) -> None:
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

    async def post(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        payload = self.encode_rpc_request(method, params)
        async with self.session.post(
            self.endpoint_uri,
            json=payload,
            timeout=self.timeout,
        ) as response:
            try:
                result = await response.json(content_type=None)
            except JSONDecodeError:
                raise BadResponseError("Couldn't decode the response into json")

            result = cast(RPCResponse, result)
            self.handle_response(result)
            return result

    async def is_connected(self) -> bool:
        result = await self.post(RPC.status, [])
        return "result" in result