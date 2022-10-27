from collections import defaultdict
from typing import DefaultDict, Type

from near.types import RPCError as RPCErrorDict


class BadResponseError(IOError):
    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class RPCError(IOError):
    def __init__(self, error: RPCErrorDict) -> None:
        self.error = error

    def __str__(self) -> str:
        return f"{self.error['message']}: {self.error['data']}"


class HandlerError(RPCError):
    ...


class RequestValidationError(RPCError):
    ...


class UnknownBlockError(HandlerError):
    ...


class ParseError(RequestValidationError):
    ...


class InternalError(RPCError):
    ...


ERRORS_BIND: DefaultDict[str, Type[RPCError]] = defaultdict(
    lambda: RPCError,
    {
        "UNKNOWN_BLOCK": UnknownBlockError,
        "PARSE_ERROR": ParseError,
        "INTERNAL_ERROR": InternalError,
    },
)
