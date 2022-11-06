import itertools
import re
from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import ValidationError

from near.exceptions import ERROR_MESSAGES_BIND, ERRORS_BIND, BadResponseError, RPCError
from near.types import ResultSchemaT, RPCEndpoint, RPCResponse


class BaseSyncProvider(ABC):
    @abstractmethod
    def call_rpc(
        self, method: RPCEndpoint, params: Any, result_schema: Type[ResultSchemaT]
    ) -> ResultSchemaT:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...


class BaseAsyncProvider(ABC):
    @abstractmethod
    async def call_rpc(
        self, method: RPCEndpoint, params: Any, result_schema: Type[ResultSchemaT]
    ) -> ResultSchemaT:
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
            "params": params,
            "id": next(self.request_counter),
        }
        return payload

    def get_result(
        self, response_dict: dict, result_schema: Type[ResultSchemaT]
    ) -> ResultSchemaT:
        # validate common response body
        try:
            response = RPCResponse(**response_dict)
        except ValidationError:
            raise BadResponseError("Bad response body")

        # handle standard errors
        error = response.error
        if error:
            raise ERRORS_BIND[error.cause.name](error)

        # check if result exists
        result_dict = response.result
        if not result_dict:
            raise BadResponseError("No result in response")

        # handle error in result dict
        error_msg = result_dict.get("error")
        if error_msg:
            for error_re, exception in ERROR_MESSAGES_BIND.items():
                if re.match(error_re, error_msg):
                    raise exception(error_msg)
            raise RPCError(error_msg)

        # validate result
        try:
            return result_schema(**result_dict)
        except ValidationError:
            raise BadResponseError("Bad result")


class BaseSyncJSONProvider(BaseJSONProvider, BaseSyncProvider):
    ...


class BaseAsyncJSONProvider(BaseJSONProvider, BaseAsyncProvider):
    ...
