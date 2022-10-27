import itertools
from abc import ABC, abstractmethod
from typing import Any

from near.exceptions import ERRORS_BIND
from near.types import RPCEndpoint, RPCResponse


class BaseSyncProvider(ABC):
    @abstractmethod
    def post(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...


class BaseAsyncProvider(ABC):
    @abstractmethod
    async def post(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        ...

    @abstractmethod
    async def is_connected(self) -> bool:
        ...


class BaseJSONProvider:
    def __init__(self) -> None:
        self.request_counter = itertools.count()

    def encode_rpc_request(self, method: RPCEndpoint, params: Any) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": next(self.request_counter),
        }
        return payload

    def handle_response(self, response: RPCResponse) -> None:
        error = response.get("error")
        if error:
            raise ERRORS_BIND[error["name"]](error)


class BaseSyncJSONProvider(BaseJSONProvider, BaseSyncProvider):
    ...


class BaseAsyncJSONProvider(BaseJSONProvider, BaseAsyncProvider):
    ...
